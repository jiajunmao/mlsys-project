# Document for Predicative Eviction for CDN Asset

## Introduction
Content Delivery Network (CDN) is a widely used technique to speed up page load, distribute data center traffic load to edge servers, and improve user experience browsing the web. However, like any other caches in the world, CDN can only be truly effective if the hit ratio is reasonably high. Multiple cache eviction policies are used in modern CDNs ranging from the traditional LRU to zoned-LRU with privileged zones. However, all of these algorithms are retrospective. For example, LRU uses a doubly-linked hashmap to keep track of the **least recently** used cache to evict.

In this project, we experiment with the idea of predicative eviction. The method uses time series analysis on access traces 

## Feasibility Analysis