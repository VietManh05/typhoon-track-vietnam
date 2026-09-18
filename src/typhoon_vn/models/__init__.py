"""Neural-network architectures for typhoon track forecasting."""

from typhoon_vn.models.baselines import CLIPERForecaster, PersistenceForecaster
from typhoon_vn.models.lstm import (
    AttentionLSTMTrackForecaster,
    LSTMTrackForecaster,
    Seq2SeqLSTMTrackForecaster,
)
from typhoon_vn.models.transformer import TransformerTrackForecaster

__all__ = [
    # LSTM family
    "LSTMTrackForecaster",
    "Seq2SeqLSTMTrackForecaster",
    "AttentionLSTMTrackForecaster",
    # Transformer
    "TransformerTrackForecaster",
    # Classical baselines
    "PersistenceForecaster",
    "CLIPERForecaster",
]
