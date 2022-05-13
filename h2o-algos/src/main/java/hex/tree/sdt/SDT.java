package hex.tree.sdt;

import hex.ModelBuilder;
import hex.ModelCategory;
import org.apache.log4j.Logger;
import water.DKV;
import water.exceptions.H2OModelBuilderIllegalArgumentException;
import water.fvec.Frame;
import water.util.*;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Single Decision Tree
 */
public class SDT extends ModelBuilder<SDTModel, SDTModel.SDTParameters, SDTModel.SDTOutput> {
    private int maxDepth;
    int nodesCount;

    private double[][] compressedTree;

    private Integer actualDepth;

    private Node root;

    private SDTModel model;
    transient Random rand;

    // todo - create file with constants ?
    private final static int LIMIT_NUM_ROWS_FOR_SPLIT = 3;

    private static final Logger LOG = Logger.getLogger(SDT.class);


    public SDT(SDTModel.SDTParameters parameters) {
        super(parameters);
        this.maxDepth = parameters.depth;
        this.actualDepth = 0;
        this.nodesCount = 0;
        this.compressedTree = null;
    }

    public double[][] compress() {
        //  if parent node is at index i in the array then the left child of that node is at index (2*i + 1) 
        //  and right child is at index (2*i + 2) in the array. 
        System.out.println("Nodes count when compressing: " + nodesCount);
        // 2^k - 1 is max count of nodes, where k is depth
        compressedTree = new double[(int) Math.pow(2, actualDepth)][2];
        writeSubtreeStartingFromIndex(root, 0);
        return compressedTree;
    }

    private void writeSubtreeStartingFromIndex(final Node actualNode, final int actualIndex) {
        if (actualNode == null) {
            return;
        }
        compressedTree[actualIndex][0] = actualNode.getFeature() == null ? -1 
                                                 : actualNode.getFeature().doubleValue();
        compressedTree[actualIndex][1] = actualNode.getFeature() == null ? actualNode.getDecisionValue().doubleValue()
                                                 : actualNode.getThreshold();
        writeSubtreeStartingFromIndex(actualNode.getLeft(), 2 * actualIndex + 1);
        writeSubtreeStartingFromIndex(actualNode.getRight(), 2 * actualIndex + 2);
    }

    public double[][] getCompressedTree() {
        if (compressedTree == null) {
            compress();
        }
        return compressedTree;
    }

    public Node buildSubtree(final Frame data, DataFeaturesLimits featuresLimits, int nodeDepth) {
        Node subtreeRoot = new Node();
        nodesCount++;
        if(actualDepth < nodeDepth) {
            actualDepth = nodeDepth;
        }
        // todo - add limit by information gain (at least because of ideal split for example 11111)
        double zeroRatio = getZeroRatio(data);
        if (actualDepth >= maxDepth || data.numRows() <= LIMIT_NUM_ROWS_FOR_SPLIT || zeroRatio > 0.9 || zeroRatio < 0.1) {
            System.out.println("actualDepth: " + actualDepth + ", data.numRows(): " + data.numRows() + ", zeroRatio: " + zeroRatio);
            if(zeroRatio >= 0.5) {
                subtreeRoot.setDecisionValue(0);
            } else if(zeroRatio < 0.5) {
                subtreeRoot.setDecisionValue(1);
            }
            return subtreeRoot;
        }
        int featuresNumber = data.numCols();

        // find split (feature and threshold)
        Pair<Double, Double> currentMinEntropyPair = new Pair<>(-1., Double.MAX_VALUE);
        int bestFeatureIndex = -1;
        for (int featureIndex = 0; featureIndex < featuresNumber - 1 /*last column is prediction*/; featureIndex++) {
            final int featureIndexForLambda = featureIndex;
            // iterate all candidate values of threshold
            Pair<Double, Double> minEntropyForFeature = featuresLimits.getFeatureRange(featureIndex)
                    .map(candidateValue -> new Pair<>(
                            candidateValue, calculateEntropyOfSplit(featureIndexForLambda, candidateValue)))
                    .min(Comparator.comparing(Pair::_2))
                    .get();
            if (minEntropyForFeature._2() < currentMinEntropyPair._2()) {
                currentMinEntropyPair = minEntropyForFeature;
                bestFeatureIndex = featureIndex;
            }
        }
        
        double threshold = currentMinEntropyPair._1();
        subtreeRoot.setFeature(bestFeatureIndex);
        subtreeRoot.setThreshold(threshold);

        // split data
        Frame split = splitData(bestFeatureIndex, threshold);
        String[] outputColNamesLeft = Arrays.stream(_train.names()).map(n -> n + "Left").toArray(String[]::new);
        String[] outputColNamesRight = Arrays.stream(_train.names()).map(n -> n + "Right").toArray(String[]::new);
        subtreeRoot.setLeft(buildSubtree(split.subframe(outputColNamesLeft),
                featuresLimits.updateMax(bestFeatureIndex, threshold), nodeDepth + 1));
        subtreeRoot.setRight(buildSubtree(split.subframe(outputColNamesRight),
                featuresLimits.updateMin(bestFeatureIndex, threshold), nodeDepth + 1));
        return subtreeRoot;
    }

    private double entropyBinarySplit(final double oneClassFrequency) {
//        System.out.println(oneClassFrequency + "..." + (oneClassFrequency < 0.01 ? 0 : (oneClassFrequency * Math.log(oneClassFrequency)))
//        + "..." + (oneClassFrequency > 0.99 ? 0 : ((1 - oneClassFrequency) * Math.log(1 - oneClassFrequency))));
//        int elementsCount = valuesCounts.values().stream().reduce(0, Integer::sum);
        return -1 * ((oneClassFrequency < 0.01 ? 0 : (oneClassFrequency * Math.log(oneClassFrequency)))
                             + (oneClassFrequency > 0.99 ? 0 : ((1 - oneClassFrequency) * Math.log(1 - oneClassFrequency))));
    }

    public double calculateEntropyOfSplit(final int featureIndex, final double threshold) {
        CountSplitValuesMRTask task = new CountSplitValuesMRTask(featureIndex, threshold);
        task.doAll(_train);

//        System.out.println(task.countLeft + " " + task.countLeft0 + " " + task.countRight + " " + task.countRight0);
//        // just count data records with needed value of feature
//        System.out.println("hh " + entropyBinarySplit(task.countLeft0 * 1.0 / (task.countLeft)) + " "
//        + task.countLeft + " " + (task.countLeft + task.countRight));
        double a1 = (entropyBinarySplit(task.countLeft0 * 1.0 / (task.countLeft))
                             * task.countLeft / (task.countLeft + task.countRight));
        double a2 = (entropyBinarySplit(task.countRight0 * 1.0 / (task.countRight))
                             * task.countRight / (task.countLeft + task.countRight));
        double value = a1 + a2;
//        System.out.println("value: " + value);
        return value;

    }

    private DataFeaturesLimits getStartFeaturesLimits() {
        return new DataFeaturesLimits(
                Arrays.stream(_train.vecs())
                        .map(v -> new FeatureLimits(v.min(), v.max())).collect(Collectors.toList()));
    }


    private class SDTDriver extends Driver {

        @Override
        public void computeImpl() {
            model = null;
            try {
                init(true);
                if(error_count() > 0) {
                    throw H2OModelBuilderIllegalArgumentException.makeFromBuilder(SDT.this);
                }
                rand = RandomUtils.getRNG(_parms._seed);
//                isolationTreeStats = new IsolationTreeStats();
                model = new SDTModel(dest(), _parms,
                        new SDTModel.SDTOutput(SDT.this));
                model.delete_and_lock(_job);
                buildSDT();
//                model._output._model_summary = createModelSummaryTable();
                LOG.info(model.toString());
            } finally {
                if(model != null)
                    model.unlock(_job);
            }
        }

        private void buildSDT() {
            root = buildSubtree(_train, getStartFeaturesLimits(), 1);
            
            CompressedSDT compressedSDT = new CompressedSDT(compress());

            model._output.treeKey = compressedSDT._key;
            DKV.put(compressedSDT);
            _job.update(1);
            model.update(_job);
        }
        
    }

    
//
//    public void trainSDT() {
//        root = buildSubtree(trainData, getStartFeaturesLimits());
////        System.out.println(root);
//    }

    @Override
    protected Driver trainModelImpl() {
        return new SDTDriver();
    }
    

    @Override
    public ModelCategory[] can_build() {
        return new ModelCategory[]{
                ModelCategory.Binomial,
//                ModelCategory.Multinomial,
//                                            ModelCategory.Ordinal,
//                ModelCategory.Regression
                };
    }

    @Override
    public boolean isSupervised() {
        return true;
    }

//    public Vec predict(final Frame data) {
//        // task to recursively apply nodes criteria to each row, so it can be parallelized by rows 
//        // (should it be parallelised one more time, not only map-reduce?)
//        PredictMRTask task = new PredictMRTask(getCompressedTree());
//        byte[] outputTypes = new byte[]{Vec.T_NUM};
//        task.doAll(outputTypes, data);
//
//        Frame result = task.outputFrame(
//                null, // The output Frame will be stored in DKV and you can access it with this Key, can be null, in case you don't wanted in DKV
//                new String[]{"outputClass"},
//                new String[][]{null} // Categorical columns need domain, pass null for Numerical and String columns
//        );
//        return result.vec(0);
//    }


    public Frame splitData(final int feature, final double threshold /* are all features double ? todo*/) {
        byte[] outputTypes = Arrays.copyOf(_train.types(), _train.types().length * 2);
        System.arraycopy(_train.types(), 0, outputTypes, _train.types().length, _train.types().length);

        String[][] outputDomains = Arrays.copyOf(_train.domains(), _train.domains().length * 2);
        System.arraycopy(_train.domains(), 0, outputDomains, _train.domains().length, _train.domains().length);
        String[] outputColNames = (Stream.concat(Arrays.stream(_train.names()).map(n -> n + "Left"),
                Arrays.stream(_train.names()).map(n -> n + "Right")).toArray(String[]::new));
        
        // Define task
        SplitFrameMRTask task = new SplitFrameMRTask(feature, threshold);
        System.out.println("trainData.types().length: " + _train.types().length);
        // Run task
        task.doAll(outputTypes, _train);
        System.out.println("Domains: " + Arrays.deepToString(_train.domains()));

        return task.outputFrame(
                null, // The output Frame will be stored in DKV and you can access it with this Key, can be null, in case you don't wanted in DKV
                outputColNames,
                outputDomains // Categorical columns need domain, pass null for Numerical and String columns
        );
    }

    private Double getZeroRatio(final Frame data) {
        GetClassCountsMRTask task = new GetClassCountsMRTask();
        task.doAll(data);
        return task.count0 * 1.0 / (task.count0 + task.count1);
    }


    public Node getRoot() {
        return root;
    }
    

}


// todo - analyze input data to get candidates for threshold
// see random forest with 1 tree
// bin data (go not by step but by count of data)
// data must be solved by histogram because of the size


// todo:
// use real dataset in test. Get score for some dataset
// train random forest on the same data to see the difference
// train sklearn decision tree on the same data
// debug dtree and see how the clustering is used
// more general - n-class classification, regression, gini, different 