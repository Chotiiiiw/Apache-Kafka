# Apache-Kafka-
Explore kafka and basic distributed system concepts.

## First exercise. Topics, Partitions, Producers, and Consumers. 
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
 ![Alt Text](/docs/images/exercise-1/first.png).

 ## Second exercise. Message key.
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
 ![Alt Text](/docs/images/exercise-2/first.png)

 ## Third Exercise. Kafka Cluster. 

- To delete "distributed-orders" topic, run this. 
```bash 
docker exec -it kafka-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --delete \
  --topic distributed-orders \
  --bootstrap-server kafka-1:29092
```

1. Start with 
```bash 
docker compose up
```
and make sure you're at exercise_3 
2. Next, check if there are 3 containers
```bash
docker compose ps
```
3. Create kafka topic called distributed-orders with 3 partitions and 3 replicas
```bash
docker exec -it kafka-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic distributed-orders \
  --partitions 3 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
4. Describe topic
```bash
docker exec -it kafka-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --describe \
  --topic distributed-orders \
  --bootstrap-server localhost:9092
```
![Alt Text](/docs/images/exercise-3/before.png)
5. Kill kafka-2 
```bash 
docker stop kafka-2
```
Check 
```bash
docker compose ps -a
```
6. Check after 1 broker died
```bash
docker exec -it kafka-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --describe \
  --topic distributed-orders \
  --bootstrap-server kafka-1:29092
```
![Alt Text](/docs/images/exercise-3/after_dead.png)
7. revive that broker 
```bash 
docker start kafka-2
```

8. Describe 
```bash 
docker exec -it kafka-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --describe \
  --topic distributed-orders \
  --bootstrap-server kafka-1:29092
```
![alt text](docs/images/exercise-3/revived.png) 

## Exercise 4. Consumer group

1. Create new topic with 5 partitions and 3 replicas 
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic consumer-lab \
  --partitions 5 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
2. Create producer with Producer with message key. 
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-console-producer.sh \
  --topic consumer-lab \
  --bootstrap-server kafka-1:29092 \
  --reader-property parse.key=true \
  --reader-property key.separator=:
``` 
- Then put these messages 
```plain text
a:1
b:2
c:3
e:3
r:2
a:3
b:8
h:10
r:11
h:6
z:3
```
4. Create with group called "order-workers"
```bash 
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic consumer-lab \
  --group order-workers \
  --bootstrap-server kafka-1:29092 \
  --formatter-property print.key=true \
  --formatter-property print.partition=true \
  --formatter-property print.offset=true \
  --formatter-property print.value=true
```

5. Create one more consumer in the group 
```bash
docker exec -it kafka-4-2 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic consumer-lab \
  --group order-workers \
  --bootstrap-server kafka-2:29092 \
  --formatter-property print.key=true \
  --formatter-property print.partition=true \
  --formatter-property print.offset=true \
  --formatter-property print.value=true
```
![alt text](/docs/images/exercise-4/zero.png)
6. Check 
```bash 
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group order-workers \
  --members \
  --verbose
```
![Alt Text](/docs/images/exercise-4/first.png)

## Exercise 4.2. Rebalance.

- Check for rebalanced
1. Check the partions for each consumer
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group order-workers \
  --members \
  --verbose
```
2. Kill one consumer B(Can be A either). with "Control + C"
3. Check again 
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group order-workers \
  --members \
  --verbose
```
![alt text](/docs/images/exercise-4/second.png)

## Exercise 4.2. Consumer Group Offset.
Continue 

1. Check current offset. 
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group order-workers
```
![alt text](docs/images/exercise-4/third.png)
Explanation: 
- CURRENT-OFFSET is the current offset. hahaha
- LOG-END-OFFSET: Where the partition data currently ends.
- LAG  = current_offset - log-end-offset

2. Kill every consumer, with "Control + C" 
3. Produce message to Producer. 
![alt text](/docs/images/exercise-4/fourth.png)
4. Check current offset again
```bash
docker exec -it kafka-4-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group order-workers
```
![alt text](docs/images/exercise-4/fifth.png)
There are lags in patition-3 and partition-4.
## Exercise 5. Delivery Semantics / Offset Commit

1. Create a topic called delivery-lab 
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic delivery-lab \
  --partitions 3 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
2. You may check 
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --describe \
  --topic delivery-lab \
  --bootstrap-server kafka-1:29092
```
![alt text](/docs/images/exercise-5/zero.png)
3. Create Producer with key
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-console-producer.sh \
  --topic delivery-lab \
  --bootstrap-server kafka-1:29092 \
  --reader-property parse.key=true \
  --reader-property key.separator=:
```

4. Create new consumer group called "delivery-workers"
```bash 
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic delivery-lab \
  --group delivery-workers \
  --from-beginning \
  --bootstrap-server kafka-1:29092 \
  --formatter-property print.partition=true \
  --formatter-property print.offset=true \
  --formatter-property print.key=true \
  --formatter-property print.value=true
```
![alt text](/docs/images/exercise-5/third.png)
5. Check commited status 
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group delivery-workers
```
![alt text](docs/images/exercise-5/first.png)
6. Stop consumer group with "control + C"
7. Offset reset (Preview)
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --group delivery-workers \
  --topic delivery-lab \
  --reset-offsets \
  --shift-by -1 \
  --dry-run
```
![alt text](docs/images/exercise-5/second.png)
 
8. Offset reset (Execute)
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --group delivery-workers-v2 \
  --topic delivery-lab \
  --reset-offsets \
  --shift-by -1 \
  --execute
```

9. Check
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic delivery-lab \
  --group delivery-workers \
  --bootstrap-server kafka-1:29092 \
  --formatter-property print.partition=true \
  --formatter-property print.offset=true \
  --formatter-property print.key=true \
  --formatter-property print.value=true
```

## Exercise 6.1. At-least-once
1. Create a topic. This time, only one partition is created. 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic atleast-once-lab \
  --partitions 1 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
2. Create producer 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-producer.sh \
  --topic atleast-once-lab \
  --bootstrap-server kafka-1:29092
```
Then send messages:
    payment-001
    payment-002
    payment-003
Then control + C
3. Create consumer with auto commit, but the commit will occur only 60 seconds.
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic atleast-once-lab \
  --group atleast-workers \
  --from-beginning \
  --bootstrap-server kafka-1:29092 \
  --command-property enable.auto.commit=false \
  --formatter-property print.offset=true \
  --formatter-property print.value=true
```
After 3 messages are shown, kill that consumer. So nothing is yet committed. 
![alt text](docs/images/exercise-6/6.1/first.png)
4. Look at commited offset. 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group atleast-workers
```
![alt text](docs/images/exercise-6/6.1/second.png)
5. Then kill the consumer and create new one 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic atleast-once-lab \
  --group atleast-workers \
  --from-beginning \
  --bootstrap-server kafka-1:29092 \
  --command-property enable.auto.commit=false \
  --formatter-property print.offset=true \
  --formatter-property print.value=true
```
![alt text](docs/images/exercise-6/6.1/third.png)

## Exercise 6.2. At-most-once 
1. Create new topic 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic atmost-once-lab \
  --partitions 1 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
2. Create Producer
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-producer.sh \
  --topic atmost-once-lab \
  --bootstrap-server kafka-1:29092
```
Then send 3 messages. 
3. Simulate with this script
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --topic atmost-once-lab \
  --group atmost-workers \
  --from-beginning \
  --bootstrap-server kafka-1:29092 \
  --max-messages 1
```
This will let consumer read 1 message, then exit. So 2 messages are not read yet.
4. Then Check with this script 
```bash
docker exec -it kafka-5-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group atmost-workers
```
![alt text](docs/images/exercise-6/6.2/first.png)
5. Kill that consumer. 
6. Create consumer that will shift offset by one. 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --group atmost-workers \
  --topic atmost-once-lab \
  --reset-offsets \
  --shift-by 1 \
  --execute
```
So this would mean that message 2 is now commited, but hasn't yet process. 
7. Describe that consumer 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server kafka-1:29092 \
  --describe \
  --group atmost-workers
```

## Exercise 6.3. Idempotent Consumer
1. Create topic 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic idempotent-lab \
  --partitions 1 \
  --replication-factor 3 \
  --bootstrap-server kafka-1:29092
```
2. Create Producer. 
```bash
docker exec -it kafka-6-1 \
  /opt/kafka/bin/kafka-console-producer.sh \
  --topic idempotent-lab \
  --bootstrap-server kafka-1:29092
```
3. Install confluent_kafka
```bash
pip install confluent-kafka
```
4. Run consumer.py
```bash
python consumer.py
```
** Make sure you're at exercise-6. 
![alt text](docs/images/exercise-6/6.3/first.png)

5. Note
This is just a simulating of idempotent consumer concept. Data is store in RAM, so it'll be deleted later after the process restarts. 