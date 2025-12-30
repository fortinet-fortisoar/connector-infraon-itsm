from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, check_health
from .constants import LOGGER_NAME

logger = get_logger(LOGGER_NAME)

class InfraonITSM(Connector):
    def execute(self, config, operation, params, **kwargs):
        try:
            config['connector_info'] = {"connector_name": self._info_json.get('name')}
            
            op_function = operations.get(operation)
            if not op_function:
                raise ConnectorError(f"Unsupported operation: {operation}")
            
            return op_function(config, params, **kwargs)
            
        except Exception as err:
            logger.error(f"Error executing action {operation}: {err}")
            raise ConnectorError(str(err))

    def check_health(self, config):
        try:
            return check_health(config)
        except Exception as e:
            raise ConnectorError(f"Health check failed: {str(e)}")