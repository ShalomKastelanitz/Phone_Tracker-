from datetime import datetime
import uuid

class InserrCalls:
    def __init__(self, driver):
        self.driver = driver

    def create_call(self, interaction_data):
        with self.driver.session() as session:
            query = """
            MERGE (from:Device {
                device_id: $from_id,
                name: $from_name,
                brand: $from_brand,
                model: $from_model,
                os: $from_os,
                latitude: $from_latitude,
                longitude: $from_longitude,
                altitude_meters: $from_altitude_meters,
                accuracy_meters: $from_accuracy_meters
            })
            MERGE (to:Device {
                device_id: $to_id,
                name: $to_name,
                brand: $to_brand,
                model: $to_model,
                os: $to_os,
                latitude: $to_latitude,
                longitude: $to_longitude,
                altitude_meters: $to_altitude_meters,
                accuracy_meters: $to_accuracy_meters
            })
            CREATE (from)-[c:CONNECTED {
                interaction_id: $interaction_id,
                method: $method,
                signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters,
                duration_seconds: $duration_seconds,
                timestamp: datetime($timestamp)
            }]->(to)
            RETURN c.interaction_id as interaction_id
            """
            fields = ['id', 'name', 'brand', 'model', 'os', 'latitude', 'longitude', 'altitude_meters', 'accuracy_meters' ]
            dct_values = {}
            for i, field in enumerate (fields):
                if i < 5:
                    dct_values[f'from_{field}'] = interaction_data['devices'][0][field]
                else:
                    dct_values[f'from_{field}'] = interaction_data['devices'][0]['location'][field]
            for i, field in enumerate(fields):
                if i < 5:
                    dct_values[f'to_{field}'] = interaction_data['devices'][1][field]
                else:
                    dct_values[f'to_{field}'] = interaction_data['devices'][1]['location'][field]
            dct_values['interaction_id'] = str(uuid.uuid4())
            dct_values['method'] = interaction_data['interaction']['method']
            dct_values['signal_strength_dbm'] = interaction_data['interaction']['signal_strength_dbm']
            dct_values['distance_meters'] = interaction_data['interaction']['distance_meters']
            dct_values['duration_seconds'] = interaction_data['interaction']['duration_seconds']
            dct_values['timestamp'] = datetime.strptime(interaction_data['interaction']['timestamp'], '%Y-%m-%dT%H:%M:%S')

            result = session.run(query, dct_values)
            return result.single()['interaction_id']