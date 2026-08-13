# Apache-Kafka-

First, you open docker, then docker compoes up. 
```bash
docker exec -it <name or id of the container> sh
```
- Create a topic called orders 
- Create 3 partitions 
- No replication-factor yet
- bootstrap-server localhost: 9092
command 
```bash
/opt/kafka/bin/kafka-topics.sh --create --topic orders --partitions 3 --bootstrap-server localhost:9092
```
Second, create producer. If you have no idea what command to use, use this to know what to do(or just ask chatgpt)
```bash
/opt/kafka/bin/kafka-console-producer.sh --help
```
This would show everything you need. 
Then run this command 
```bash
/opt/kafka/bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092
```
So the producer is created.

Third, create customer. Similaryly, If you don't know what command to use, run this 
```bash
/opt/kafka/bin/kafka-console-customer.sh --help
```
Then run this to create customer. No offset, run from the beginning. 
```bash
/opt/kafka/bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092
```

This is the result when producer and customer are connected to orders topic.  (left is producer, right is customer)
 ![Alt Text](/docs/images/first.png).