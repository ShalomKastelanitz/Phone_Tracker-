class Queries:
    def __init__(self, driver):
        self.driver = driver

    def get_bluetooth_connections(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (start:Device)
                MATCH (end:Device)
                WHERE start <> end
                MATCH path = shortestPath((start)-[:INTERACTED_WITH*]->(end))
                WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
                WITH path, length(path) as pathLength
                ORDER BY pathLength DESC
                LIMIT 1
                RETURN length(path) as lennnn
            """)
            record = result.single()
            return {"bluetooth_connection_length": record['lennnn'] if record else 0}

    def find_relationships_with_signal_strength(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Device)-[r:INTERACTED_WITH]-(d2:Device)
                WHERE r.signal_strength_dbm > -60
                RETURN r.id AS rId, d.id AS deviceId, d2.id AS connectedDeviceId, r.signal_strength_dbm as signal_strength_dbm
            """)
            return [{"id": record['rId'], "from": record['deviceId'],
                     "to": record['connectedDeviceId'],
                     "signalStrength": record['signal_strength_dbm']} for record in result]


    def count_connected_devices(self, device_id):
        device_id = device_id.strip()

        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Device)-[:INTERACTED_WITH]-(connected_device:Device)
                WHERE d.id = $device_id 
                RETURN COUNT(connected_device) AS connected_count
            """, device_id=device_id)
            record = result.single()
            return {"connected_devices_count": record['connected_count']} if record else {"connected_devices_count": 0}


    def is_direct_connection(self, device_id_1, device_id_2):
        device_id_1 = device_id_1.strip()
        device_id_2 = device_id_2.strip()

        with self.driver.session() as session:
            result = session.run("""
                MATCH (d1:Device)-[:INTERACTED_WITH]-(d2:Device)
                WHERE d1.id = $device_id_1 AND d2.id = $device_id_2
                RETURN d1, d2
            """, device_id_1=device_id_1, device_id_2=device_id_2)
            record = result.single()
            return True if record else False

    def get_last_device_connection(self, device_id):
        device_id = device_id.strip()

        with self.driver.session() as session:
            result = session.run("""
                MATCH (n:Device)-[r:INTERACTED_WITH]-(n2:Device)
                WHERE n.id = $device_id
                RETURN r.timestamp AS timestamp, properties(r) AS r_properties
                ORDER BY r.timestamp DESC
                LIMIT 1
            """, device_id=device_id)

            record = result.single()

            if not record:
                return None


            timestamp = record["timestamp"] if record["timestamp"] else None

            return {
                'timestamp': timestamp,
                'properties': record["r_properties"]
            }