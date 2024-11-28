from datetime import datetime
import uuid

class CallsHandlerRepository:
    def __init__(self, driver):
        self.driver = driver

    def save_call(self, call_data):
        with self.driver.session() as session:
            query = """
            MERGE (caller:Device {
                device_id: $caller_id,
                name: $caller_name,
                brand: $caller_brand,
                model: $caller_model,
                os: $caller_os,
                latitude: $caller_latitude,
                longitude: $caller_longitude,
                altitude_meters: $caller_altitude_meters,
                accuracy_meters: $caller_accuracy_meters
            })
            MERGE (receiver:Device {
                device_id: $receiver_id,
                name: $receiver_name,
                brand: $receiver_brand,
                model: $receiver_model,
                os: $receiver_os,
                latitude: $receiver_latitude,
                longitude: $receiver_longitude,
                altitude_meters: $receiver_altitude_meters,
                accuracy_meters: $receiver_accuracy_meters
            })
            CREATE (caller)-[c:CONNECTED {
                call_id: $call_id,
                method: $method,
                signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters,
                duration_seconds: $duration_seconds,
                timestamp: datetime($timestamp)
            }]->(receiver)
            RETURN c.call_id as call_id
            """
            fields = ['id', 'name', 'brand', 'model', 'os', 'latitude', 'longitude', 'altitude_meters', 'accuracy_meters']
            dct_values = {}

            for i, field in enumerate(fields):
                if i < 5:
                    dct_values[f'caller_{field}'] = call_data['devices'][0][field]
                else:
                    dct_values[f'caller_{field}'] = call_data['devices'][0]['location'][field]

            for i, field in enumerate(fields):
                if i < 5:
                    dct_values[f'receiver_{field}'] = call_data['devices'][1][field]
                else:
                    dct_values[f'receiver_{field}'] = call_data['devices'][1]['location'][field]

            dct_values['call_id'] = str(uuid.uuid4())
            dct_values['method'] = call_data['interaction']['method']
            dct_values['signal_strength_dbm'] = call_data['interaction']['signal_strength_dbm']
            dct_values['distance_meters'] = call_data['interaction']['distance_meters']
            dct_values['duration_seconds'] = call_data['interaction']['duration_seconds']
            dct_values['timestamp'] = datetime.strptime(call_data['interaction']['timestamp'], '%Y-%m-%dT%H:%M:%S')

            result = session.run(query, dct_values)
            return result.single()['call_id']
