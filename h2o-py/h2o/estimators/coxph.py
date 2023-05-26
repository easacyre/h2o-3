#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  GNU Affero General Public License v3 (see LICENSE for details)
#

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OCoxProportionalHazardsEstimator(H2OEstimator):
    """
    Cox Proportional Hazards

    Trains a Cox Proportional Hazards Model (CoxPH) on an H2O dataset.
    """

    algo = "coxph"
    supervised_learning = True

    def __init__(self,
                 model_id=None,  # type: Optional[Union[None, str, H2OEstimator]]
                 training_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 start_column=None,  # type: Optional[str]
                 stop_column=None,  # type: Optional[str]
                 response_column=None,  # type: Optional[str]
                 ignored_columns=None,  # type: Optional[List[str]]
                 weights_column=None,  # type: Optional[str]
                 offset_column=None,  # type: Optional[str]
                 stratify_by=None,  # type: Optional[List[str]]
                 ties="efron",  # type: Literal["efron", "breslow"]
                 init=0.0,  # type: float
                 lre_min=9.0,  # type: float
                 max_iterations=20,  # type: int
                 interactions=None,  # type: Optional[List[str]]
                 interaction_pairs=None,  # type: Optional[List[tuple]]
                 interactions_only=None,  # type: Optional[List[str]]
                 use_all_factor_levels=False,  # type: bool
                 export_checkpoints_dir=None,  # type: Optional[str]
                 single_node_mode=False,  # type: bool
                 ):
        """
        :param model_id: Destination id for this model; auto-generated if not specified.
               Defaults to ``None``.
        :type model_id: Union[None, str, H2OEstimator], optional
        :param training_frame: Id of the training data frame.
               Defaults to ``None``.
        :type training_frame: Union[None, str, H2OFrame], optional
        :param start_column: Start Time Column.
               Defaults to ``None``.
        :type start_column: str, optional
        :param stop_column: Stop Time Column.
               Defaults to ``None``.
        :type stop_column: str, optional
        :param response_column: Response variable column.
               Defaults to ``None``.
        :type response_column: str, optional
        :param ignored_columns: Names of columns to ignore for training.
               Defaults to ``None``.
        :type ignored_columns: List[str], optional
        :param weights_column: Column with observation weights. Giving some observation a weight of zero is equivalent
               to excluding it from the dataset; giving an observation a relative weight of 2 is equivalent to repeating
               that row twice. Negative weights are not allowed. Note: Weights are per-row observation weights and do
               not increase the size of the data frame. This is typically the number of times a row is repeated, but
               non-integer values are supported as well. During training, rows with higher weights matter more, due to
               the larger loss function pre-factor. If you set weight = 0 for a row, the returned prediction frame at
               that row is zero and this is incorrect. To get an accurate prediction, remove all rows with weight == 0.
               Defaults to ``None``.
        :type weights_column: str, optional
        :param offset_column: Offset column. This will be added to the combination of columns before applying the link
               function.
               Defaults to ``None``.
        :type offset_column: str, optional
        :param stratify_by: List of columns to use for stratification.
               Defaults to ``None``.
        :type stratify_by: List[str], optional
        :param ties: Method for Handling Ties.
               Defaults to ``"efron"``.
        :type ties: Literal["efron", "breslow"]
        :param init: Coefficient starting value.
               Defaults to ``0.0``.
        :type init: float
        :param lre_min: Minimum log-relative error.
               Defaults to ``9.0``.
        :type lre_min: float
        :param max_iterations: Maximum number of iterations.
               Defaults to ``20``.
        :type max_iterations: int
        :param interactions: A list of predictor column indices to interact. All pairwise combinations will be computed
               for the list.
               Defaults to ``None``.
        :type interactions: List[str], optional
        :param interaction_pairs: A list of pairwise (first order) column interactions.
               Defaults to ``None``.
        :type interaction_pairs: List[tuple], optional
        :param interactions_only: A list of columns that should only be used to create interactions but should not
               itself participate in model training.
               Defaults to ``None``.
        :type interactions_only: List[str], optional
        :param use_all_factor_levels: (Internal. For development only!) Indicates whether to use all factor levels.
               Defaults to ``False``.
        :type use_all_factor_levels: bool
        :param export_checkpoints_dir: Automatically export generated models to this directory.
               Defaults to ``None``.
        :type export_checkpoints_dir: str, optional
        :param single_node_mode: Run on a single node to reduce the effect of network overhead (for smaller datasets)
               Defaults to ``False``.
        :type single_node_mode: bool
        """
        super(H2OCoxProportionalHazardsEstimator, self).__init__()
        self._parms = {}
        self._id = self._parms['model_id'] = model_id
        self.training_frame = training_frame
        self.start_column = start_column
        self.stop_column = stop_column
        self.response_column = response_column
        self.ignored_columns = ignored_columns
        self.weights_column = weights_column
        self.offset_column = offset_column
        self.stratify_by = stratify_by
        self.ties = ties
        self.init = init
        self.lre_min = lre_min
        self.max_iterations = max_iterations
        self.interactions = interactions
        self.interaction_pairs = interaction_pairs
        self.interactions_only = interactions_only
        self.use_all_factor_levels = use_all_factor_levels
        self.export_checkpoints_dir = export_checkpoints_dir
        self.single_node_mode = single_node_mode

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``Union[None, str, H2OFrame]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')

    @property
    def start_column(self):
        """
        Start Time Column.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("start_column")

    @start_column.setter
    def start_column(self, start_column):
        assert_is_type(start_column, None, str)
        self._parms["start_column"] = start_column

    @property
    def stop_column(self):
        """
        Stop Time Column.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("stop_column")

    @stop_column.setter
    def stop_column(self, stop_column):
        assert_is_type(stop_column, None, str)
        self._parms["stop_column"] = stop_column

    @property
    def response_column(self):
        """
        Response variable column.

        Type: ``str``.
        """
        return self._parms.get("response_column")

    @response_column.setter
    def response_column(self, response_column):
        assert_is_type(response_column, None, str)
        self._parms["response_column"] = response_column

    @property
    def ignored_columns(self):
        """
        Names of columns to ignore for training.

        Type: ``List[str]``.
        """
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, ignored_columns):
        assert_is_type(ignored_columns, None, [str])
        self._parms["ignored_columns"] = ignored_columns

    @property
    def weights_column(self):
        """
        Column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the
        dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative
        weights are not allowed. Note: Weights are per-row observation weights and do not increase the size of the data
        frame. This is typically the number of times a row is repeated, but non-integer values are supported as well.
        During training, rows with higher weights matter more, due to the larger loss function pre-factor. If you set
        weight = 0 for a row, the returned prediction frame at that row is zero and this is incorrect. To get an
        accurate prediction, remove all rows with weight == 0.

        Type: ``str``.
        """
        return self._parms.get("weights_column")

    @weights_column.setter
    def weights_column(self, weights_column):
        assert_is_type(weights_column, None, str)
        self._parms["weights_column"] = weights_column

    @property
    def offset_column(self):
        """
        Offset column. This will be added to the combination of columns before applying the link function.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  offset_column="transplant")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("offset_column")

    @offset_column.setter
    def offset_column(self, offset_column):
        assert_is_type(offset_column, None, str)
        self._parms["offset_column"] = offset_column

    @property
    def stratify_by(self):
        """
        List of columns to use for stratification.

        Type: ``List[str]``.
        """
        return self._parms.get("stratify_by")

    @stratify_by.setter
    def stratify_by(self, stratify_by):
        assert_is_type(stratify_by, None, [str])
        self._parms["stratify_by"] = stratify_by

    @property
    def ties(self):
        """
        Method for Handling Ties.

        Type: ``Literal["efron", "breslow"]``, defaults to ``"efron"``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  ties="breslow")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("ties")

    @ties.setter
    def ties(self, ties):
        assert_is_type(ties, None, Enum("efron", "breslow"))
        self._parms["ties"] = ties

    @property
    def init(self):
        """
        Coefficient starting value.

        Type: ``float``, defaults to ``0.0``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  init=2.9)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("init")

    @init.setter
    def init(self, init):
        assert_is_type(init, None, numeric)
        self._parms["init"] = init

    @property
    def lre_min(self):
        """
        Minimum log-relative error.

        Type: ``float``, defaults to ``9.0``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  lre_min=5)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("lre_min")

    @lre_min.setter
    def lre_min(self, lre_min):
        assert_is_type(lre_min, None, numeric)
        self._parms["lre_min"] = lre_min

    @property
    def max_iterations(self):
        """
        Maximum number of iterations.

        Type: ``int``, defaults to ``20``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  max_iterations=50)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations

    @property
    def interactions(self):
        """
        A list of predictor column indices to interact. All pairwise combinations will be computed for the list.

        Type: ``List[str]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interactions = ['start','stop']
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interactions=interactions)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interactions")

    @interactions.setter
    def interactions(self, interactions):
        assert_is_type(interactions, None, [str])
        self._parms["interactions"] = interactions

    @property
    def interaction_pairs(self):
        """
        A list of pairwise (first order) column interactions.

        Type: ``List[tuple]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interaction_pairs = [("start","stop")]
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interaction_pairs=interaction_pairs)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interaction_pairs")

    @interaction_pairs.setter
    def interaction_pairs(self, interaction_pairs):
        assert_is_type(interaction_pairs, None, [tuple])
        self._parms["interaction_pairs"] = interaction_pairs

    @property
    def interactions_only(self):
        """
        A list of columns that should only be used to create interactions but should not itself participate in model
        training.

        Type: ``List[str]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interactions = ['start','stop']
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interactions_only=interactions)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interactions_only")

    @interactions_only.setter
    def interactions_only(self, interactions_only):
        assert_is_type(interactions_only, None, [str])
        self._parms["interactions_only"] = interactions_only

    @property
    def use_all_factor_levels(self):
        """
        (Internal. For development only!) Indicates whether to use all factor levels.

        Type: ``bool``, defaults to ``False``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  use_all_factor_levels=True)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("use_all_factor_levels")

    @use_all_factor_levels.setter
    def use_all_factor_levels(self, use_all_factor_levels):
        assert_is_type(use_all_factor_levels, None, bool)
        self._parms["use_all_factor_levels"] = use_all_factor_levels

    @property
    def export_checkpoints_dir(self):
        """
        Automatically export generated models to this directory.

        Type: ``str``.

        :examples:

        >>> import tempfile
        >>> from os import listdir
        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> checkpoints_dir = tempfile.mkdtemp()
        >>> coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                            stop_column="stop",
        ...                                            export_checkpoints_dir=checkpoints_dir)
        >>> coxph.train(x=predictor,
        ...             y=response,
        ...             training_frame=heart)
        >>> len(listdir(checkpoints_dir))
        """
        return self._parms.get("export_checkpoints_dir")

    @export_checkpoints_dir.setter
    def export_checkpoints_dir(self, export_checkpoints_dir):
        assert_is_type(export_checkpoints_dir, None, str)
        self._parms["export_checkpoints_dir"] = export_checkpoints_dir

    @property
    def single_node_mode(self):
        """
        Run on a single node to reduce the effect of network overhead (for smaller datasets)

        Type: ``bool``, defaults to ``False``.
        """
        return self._parms.get("single_node_mode")

    @single_node_mode.setter
    def single_node_mode(self, single_node_mode):
        assert_is_type(single_node_mode, None, bool)
        self._parms["single_node_mode"] = single_node_mode


    @property
    def baseline_hazard_frame(self):
        if (self._model_json is not None
                and self._model_json.get("output", {}).get("baseline_hazard", {}).get("name") is not None):
            baseline_hazard_name = self._model_json["output"]["baseline_hazard"]["name"]
            return H2OFrame.get_frame(baseline_hazard_name)

    @property
    def baseline_survival_frame(self):
        if (self._model_json is not None
                and self._model_json.get("output", {}).get("baseline_survival", {}).get("name") is not None):
            baseline_survival_name = self._model_json["output"]["baseline_survival"]["name"]
            return H2OFrame.get_frame(baseline_survival_name)
