# Apache-Kafka-

## first exercise
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

 ## Second exercise, let's try Message key
Create new topic called key-orders, since orders topic has previous message. So the output would be confusing. 
```bash
/opt/kafka/bin/kafka-topics.sh --create --topic key-orders --partitions 3 --bootstrap-server localhost:9092
```
Create new producer 
```bash
/opt/kafka/bin/kafka-console-producer.sh --topic key-orders --bootstrap-server localhost:9092 --reader-property parse.key=true --reader-property key.separator=:
```
Then try put these message
```plain text
user-1:A
user-2:B
user-3:C
user-1:D
user-2:E
user-3:F
user-1:G
user-2:H
user-3:I
```
Then create consumer
```bash
/opt/kafka/bin/kafka-console-consumer.sh --topic key-orders --from-beginning --bootstrap-server localhost:9092 --formatter-property print.key=true --formatter-property print.partition=true --formatter-property print.offset=true --formatter-property print.value=true
```
Result. At first, it looked like there a problem, but when I tried more message, it's fine. Same key -> Same partition.
 ![Alt Text](/docs/images/second.png)