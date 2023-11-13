# UV Architectural Constraints

<!-- TOC -->

- [UV Architectural Constraints](#uv-architectural-constraints)
  - [Introduction](#introduction)
  - [Summary of Constraints](#summary-of-constraints)
  - [Driving Architectural Characteristics](#driving-architectural-characteristics)
    - [#1 Evolvability](#1-evolvability)
    - [#2 Agility](#2-agility)
    - [#3 Extensibility/Composability](#3-extensibilitycomposability)
    - [#4 Integratability](#4-integratability)
      - [Other Important (non-driving) Characteristics](#other-important-non-driving-characteristics)
  - [Architectural Patterns](#architectural-patterns)
    - [Microservices](#microservices)
      - [Hybrid/Event-Driven Microservices](#hybridevent-driven-microservices)
      - [Microservice Constraints](#microservice-constraints)
      - [Further Reading on Microservices](#further-reading-on-microservices)
    - [REST/ROA](#restroa)
      - [REST constraints](#rest-constraints)
      - [Further Reading on REST/ROA](#further-reading-on-restroa)
    - [Linked Data](#linked-data)
      - [Linked Data Constraints](#linked-data-constraints)

<!-- /TOC -->

## Introduction

The purpose of this document is to outline key architectural constraints on project-uv with links to dive deeper into each one.

## Summary of Constraints

* System components follow the [Microservices Architecture](#microservice-constraints)
* Kafka is the source of truth (microservice databases are _projections_ of truth)
* UV system components follow the [REST architectural style](#restroa)
  * API interactions are RESTful and all interfaces utilize the resource abstraction
* All data in UV follows [Linked Data Principles](#linked-data)

## Driving Architectural Characteristics

Project UV can be succinctly described as an extensible, evolvable knowledge-graph. A good introduction can be found here [The Architecture vision of UV](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/6745/0005-uv-architecture-vision).

Although there are many architectural _"-illities"_ (a.k.a. architectural characteristics that are important, it is crucial to identify the driving architectural characteristics. Software architecture is a game of trade-offs, improve one characteristic typically comes at the cost of deteriorating another. This document enumerates core architectural patterns--and the constraints they imply--have been chosen to favor the driving architectural characteristics; partial explanations are detailed in the sections below. These constraints must not be violated without explicit, written architectural approval.

### #1 Evolvability

Evolution is a word most commonly associated with the concept of incremental change of an entity over time.

In truth, the overall vision of project UV is vast. There is much functionality we wish to build but we must approach this in an incremental fashioned. Evolvability allows us to balance short term goals (such as milestone deliveries for Cummins and Chevron) against the long-term vision. This chacterestic allows us to build features for today that serve as stepping-stones toward the longer-term vision. We must build our components in a way that allows us to use them in new ways that were not always known at design time.

Building new features in UV must ultimately move us forward to the next set of the adjacent possible.

### #2 Agility

Agility is the ability for the system to change as customer needs change, or when new needs are identified.

UV is an ever-evolving knowledge platform. The reality we face today is we simply do not know what UV will look like in three years time. UV unlike traditional information systems and, as such, UV will give our customers tools and capabilities they have never had before. Once they have their first taste of this power, they will dream up new and inventive questions to ask of their organization's entire body of knowledge. The optimum architecture decisions give us the power to deliver these new capabilities almost as fast as our customers can think of them.

Because this is an entirely new type of information system, built using very new technologies, we must follow an architecture that allows us to experiment, fail, learn, grow, and evolve--quickly. The UV MVP is the first of many experiments designed to figure out how to best solve our customers' problems. Often we will implement a given feature one way, demo said feature to the customer, and receive feedback. Based on that feedback we will learn more about what we're building and often make significant changes in the process.

Agility is generally achieved by improving:

* Modularity
* Testability
* Deployability
* Evolvability

By building a highly modular system with well-defined boundaries and interfaces, it becomes dramatically easier and low-risk to add new features to the system, or change existing behavior.  

### #3 Extensibility/Composability

Extensibility is defined as the ability to add functionality to a system. Dynamic extensibility implies that functionality can be added to a deployed system without impacting the rest of the system. Extensibility is induced within an architectural style by reducing the coupling between components, as exemplified by event-based integration.

Composability is the ability to combine components or data dynamically to elicit new capabilities in the system by composing services or data.

These capabilities enable the exponential growth of capabilities of the UV platform and allows us to innovate rapidly as the system as a whole scales.

### #4 Integratability

Much of Project UV involves integrating with our customer's source systems. Being able to efficiently and effective integrate these systems both to initially populate the system as well as to ingest changes is crucial for the success of this project.

#### Other Important (non-driving) Characteristics

* Scalability
* Security
* Elasticity
* Configurability
* Portability
* Visibility
* Fault-tolerance
* Performance

Non-driving characteristics are important, but trade-offs that impact the [driving characteristics](#driving-architectural-characteristics) should be made to favor those driving characteristics.

## Architectural Patterns

### Microservices

A microservice is defined as a single-purpose, independently deployable, unit of software that does one thing (and one thing only) _really well._ In short, microservices takes the single-responsibility principle to the application level.

The microservice architecture pattern is uniquely strong in key [architectural characteristics](#uv-architectural-constraints), particularly [evolvability](#1-evolvability), [agility](#2-agility), [composability](#3-extensibilitycomposibility), Modularity, Scalability, Elasticity, Testability, and Fault tolerance.

The core concept behind microservices is extreme decoupling. Each microservice is essentially developed and deployed as a stand-alone application that uses a dedicated, isolated database. Service development should be fully autonomous. Each service boundary typically corresponds to a business domain.

Although extreme decoupling introduces several benefits to the overall system, several key trade-offs are made:

Performance is one of the big trade-offs of the microservice architecture. Network calls take longer than method calls and security verification at every endpoint adds additional processing time.

Efficiency is also adversely affected. DRY (Don't Repeat Yourself) is a common design principle in software engineering. A common mistake made by developers new to this architecture is a tendency to create shared libraries, SDKs, databases, or to reuse superficially similar services beyond their defined bounded context. Although in other architectural patterns these might be useful practices, in microservices the all introduce coupling between services and components that undermines this architectural pattern's entire _raison d'etre._

In a microservice-based system, you will duplicate code. You will duplicate data. You will deploy services that are superficially similar (especially at the beginning of their lifecycle). These are very deliberate decisions inherent to this architecture pattern.

Finally, because microservices are a distributed architecture (both in terms of code and data), it becomes necessary to embrace the idea of eventual consistency.

#### Hybrid/Event-Driven Microservices

In UV, our microservices combine elements of [event-driven](https://www.youtube.com/watch?v=STKCRSUsyP0) architecture and [event-sourcing](https://www.youtube.com/watch?v=8JKjvY4etTY) systems, using [[Kafka]] as our data backplane.

An example of what this type of hybrid architecture looks like can be seen in this video: [Design Microservice Architectures the Right Way](https://www.youtube.com/watch?v=j6ow-UemzBc).

#### Microservice Constraints

* Each microservice are single-purpose maintained by a single team
* A microservice owns it's own data/database
  * Only that microservice may directly access that service's database
* Microservices only communicate via Kafka events or API calls
  * Inter-service communication should prefer consuming Kafka events
  * API contracts and Kafka messages are first-class concerns and should be designed independent of implementation
  * Kafka Messages are events, not commands
    * Kafka Messages must be idempotent
  * Kafka is the source-of-truth
  * Kafka consumers don't know about producers, Kafka producers don't know about consumers
* Microservices should be developed and deployed in isolation
* Avoid distributed transactions

#### Further Reading on Microservices

* [Managing Data in Microservices](https://www.youtube.com/watch?v=E8-e-3fRHBw)
* [Microservices Antipatterns and Pitfalls - Mark Richards](https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/)
* [Designing Event-Driven Systems](https://www.confluent.io/designing-event-driven-systems/)
* [Building Microservices: Designing Fine-Grained Systems - Sam Newman](https://www.amazon.com/Building-Microservices-Designing-Fine-Grained-Systems/dp/B09RTQY7SX/)
* [The Tao of Microservices - Richard Rodger](https://www.amazon.com/Tao-Microservices-Richard-Rodger-ebook/dp/B09782R7M2/)

### REST/ROA

When many people think about [REST](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/6748/0008-why-rest) they typically think about JSON APIs that communicate over HTTP. In truth there is much more to REST than JSON/HTTP and most APIs that self-describe as "RESTful" aren't.

[REST](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/6748/0008-why-rest) and [Resource-Oriented Architecture](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents?wikiVersion=GBmain&pagePath=/docs/Architecture%20Documentation%20and%20Guidance/0006%20why%20roa) dramatically improve many of our driving architectural characteristics, particularly [Evolvability](#1-evolvability), [Agility](#2-agility), [Extensibility/Composability](#3-extensibilitycomposibility), as well as well as improving many of our [non-driving architectural characteristics](#other-important-non-driving-chacteristics).

The [constraints](#rest-constraints) inform how we build our APIs. RESTful APIs provide an essential abstraction between our APIs and the implementation details of a given experiment. Truly RESTful APIs allow us to:

* Evolve code without breaking integration
* Create dynamic UIs that automatically respond to change in the system
* Connect all resources in UV to each other which, in turn allows us to
  * Create increasingly complex composite resources
  * Unlock new capabilities in the system as we build new services.
* Achieve all of the crucial system qualities defined in the [Why Resource Oriented Architecture](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents?wikiVersion=GBmain&pagePath=/docs/Architecture%20Documentation%20and%20Guidance/0006%20why%20roa) guidance document, namely:
  * Performance
  * Scalability
  * Simplicity
  * Modifiability
  * Evolvability
  * Extensibility
  * Customizability
  * Configurability
  * Reusability
  * Reliability

#### REST constraints

The REST architectural style is defined by six architectural constraints

* Applications follow the **client-server** architecture
* Services are **stateless**
* "safe" requests (i.e. API requests that do not have side-effects like GET) can be **cached**
* All components in UV implement a global **Uniform Interface**
  * RPC-style APIs are prohibited
  * URIs identify resources, not API endpoints
  * Resources are manipulated through representations
  * Messages and API representations are self-descriptive (serialized using JSON-LD or other [RDF](#linked-data)compatible serialization)
  * Hypermedia as the engine of application state (the chosen hypermedia format in UV is Hydra)
* Layered System
* (Optional) Code-on Demand

#### Further Reading on REST/ROA

* [The Rest of ReST - Dylan Beattie](https://www.youtube.com/watch?v=g8E1B7rTZBI)
* [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/fielding_dissertation.pdf?msclkid=725deea0bc4c11ecbf5cd27fb23e79a5)
* [UV REST API style guide](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/9073/API-Style-Guide)

### Linked Data

Linked data is a specific form of structured data that is interlinked with other data so it becomes more useful through semantic queries. Linked data builds on top of several existing standards including HTTP, [RDF](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/6747/0007-why-rdf), and URIs; but rather than using them to serve web pages only for human readers, it extends them to share information in a way that can be read automatically by computers. Linked data not only enables us to build a highly [composable](#3-extensibilitycomposibility), [evolvable](#1-evolvability) system; but also enables true knowledge representation and reasoning which are capabilities at the heart of the vision of Project UV. Linked data also solves many common data integration problems dramatically improving our [integratability](#4-integratability).

#### Linked Data Constraints

* All conceptual things (parts, documents, concepts, individuals, organizations, terms, etc.) are identified using URIs
* HTTP URIs should be used to allow these things to be looked up, interpreted, and subsequently "dereferenced".
* Useful information about what a name identifies should be provided through open standards such as [RDF](https://dev.azure.com/pdd-ihsmarkit/EPD/_wiki/wikis/UV%20Architecture%20Documents/6747/0007-why-rdf), SPARQL, etc.
* When exposing data via APIs, Kafka messages, etc.; other things should be referred to using their HTTP URI-based names
* URIs do not change
