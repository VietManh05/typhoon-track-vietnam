class WeatherProviderError(RuntimeError):
    pass


class ProviderUnavailableError(WeatherProviderError):
    pass


class LocationNotFoundError(WeatherProviderError):
    pass


class ProviderQuotaError(WeatherProviderError):
    pass
