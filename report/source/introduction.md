# Document for Predicative Eviction for CDN Asset

## Introduction
Content Delivery Network (CDN) is a widely used technique to speed up page load, distribute data center traffic load to edge servers, and improve user experience browsing the web. However, like any other caches in the world, CDN can only be truly effective if the hit ratio is reasonably high. Multiple cache eviction policies are used in modern CDNs ranging from the traditional LRU to zoned-LRU with privileged zones. However, all of these algorithms are retrospective. For example, LRU uses a doubly-linked hashmap to keep track of the **least recently** used cache to evict.

In this project, we experiment with the idea of **predicative eviction**. The method uses time series analysis on the past access traces to predict future access patterns before evicting them from the cache.

## Related Works
A few attempts have been made at this topic. **FILL**

## Least Likely Used Eviction
At the core of the predicative eviction CDN is the LLU, which is a really simple idea. LRU evicts the asset that is **least recently** used. On the other hand, LLU evicts the asset that is **least likely to be used in the future**. This aims to eliminate the problem that there is some possibility that a least recently used cache will be used in the near future while not least recently used will not.

We use LSTM to infer the access pattern of the next 2.5 minutes given the the access pattern in the past 5 minutes. We then compare the access pattern across all the cached asset, and then evict the asset with the lowest probability, regardless whether that asset has been recently used or not. We also multiply the probability with the size of the asset such that 

## Methodology
The project efforts are separated into three parts with their implementation details explained below.

### Trace Generation
We have realized from the start of the project that real-world CDN traces are hard to obtain if not possible. Therefore, we decided that we are going to complete the project on synthetic traces. Three tech stacks are used to capture network access traces
- Selenium: navigate the webpages and process HTML
- Browsermob-proxy: serve as the proxy between Selenium and browser driver to capture Http Archive Format(HAR), which contains traces to all the assets a webpage requests and loads upon visit
- A pub/sub architecture generator: we simulate concurrent user access to a website through a multi-threaded pub/sub architecture trace generator.

The generator is implemented with the following psedocode

```python
fifo_queue := []

populate_queue(fifo_queue, num_user)

foreach num_worker:
    while fifo_queue not empty:

        event := fifo_queue.pop()
        # Visit webpage and generate HAR
        visit_website(event)
        # Generate next event
        next_event := gen_next_event(event)

        fifo_queue.push(next_event)
```

We can then initialize the number worker to be something appropriate. `event` contains a few critical attributes such as the url that we want to visit, the current simulated timestamp, etc. It is important to note that the time is simulation not, _not_ wall time. Number of user controls how many concurrent user access we are simulating.

#### User Access Pattern
We also need to assume some access patterns for our users. Due to project time constraint, we only can simulate a quite non-smart user. The following statement defines the user behavior.

User will start a browsing session. A browsing session consists of a series of bursty clicks. After each click, the user needs sometime to read through the newly loaded website. The intervals between the bursty clicks are modeled by $\mathcal{N}(1m,0.5m)$. The number of clicks in a session is modeled by $\text{rand}(1,10]$. After a each browsing session, the user will take a rest before starting the next browser session. The rest interval is modeled by $\mathcal{N}(40m,20m)$.



## Feasibility Analysis