"""Build preprocessing pipelines for the modeling examples and exercises."""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_preprocessor(categorical, numeric=(), extra=()):
    """Return an unfitted encoder and scaler for the selected predictors."""
    transformers = []
    if categorical:
        transformers.append((
            "categorical", OneHotEncoder(handle_unknown="ignore"), categorical,
        ))
    if numeric:
        transformers.append(("numeric", StandardScaler(), numeric))
    transformers.extend(extra)
    return ColumnTransformer(transformers)
