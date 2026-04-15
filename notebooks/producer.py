from kafka import KafkaProducer
import json, random, time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sklepy = ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław']
kategorie = ['elektronika', 'odzież', 'żywność', 'książki']

def generate_transaction():
    if random.random() < 0.05:
        return { #podejrzana
            'tx_id': f'TX{random.randint(1000,9999)}',
            'user_id': f'u{random.randint(1,20):02d}',
            'amount': round(random.uniform(3000.0, 5000.0), 2),
            'store': random.choice(sklepy),
            'category': 'elektronika',
            'hour': random.randint(0,5),
            'timestamp': datetime.now().isoformat(),
            'is_suspicious': True
        }
    else: #normalna
        return {
            'tx_id': f'TX{random.randint(1000,9999)}',
            'user_id': f'u{random.randint(1,20):02d}',
            'amount': round(random.uniform(5.0, 5000.0), 2),
            'store': random.choice(sklepy),
            'category': random.choice(kategorie),
            'hour': random.randint(0,23),
            'timestamp': datetime.now().isoformat(),
            'is_suspicious': False
        }
for i in range(1000):
    tx = generate_transaction()
    producer.send('transactions', value=tx)
    label = "PODEJRZANA" if tx['is_suspicious'] else ""
    print(f"[{i+1}] {tx['tx_id']} | {tx['amount']:.2f} PLN | {tx['store']} | {tx['category']} | h:{tx['hour']} {label}")
    time.sleep(0.5)

producer.flush()
producer.close()
