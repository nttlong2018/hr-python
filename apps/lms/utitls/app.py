class app:
    def get_info(self):
        import configuration
        return configuration.get_app_info(__file__)