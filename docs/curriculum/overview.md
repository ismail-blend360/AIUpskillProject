# AI Agent Onboarding - v3.3 Self-Paced Edition (with SOLID)

**Learn AI engineering after work, including software design fundamentals**

⏰ **Time Commitment:** 1-2 hours per evening, 5 weeks  
📊 **Total Hours:** 35-50 hours  
🎯 **Goal:** Core skills + software design principles, sustainable pace  

---

## 🎯 What Changed from v3.2

### **Added Back: SOLID Refactoring Week**
- Week 2 dedicated to software design
- Refactor your Milestone 1 code
- Learn all 5 SOLID principles
- Apply design patterns
- Still time-boxed for evenings

### **New Structure:**
- v3.2: 4 weeks, 5 milestones
- **v3.3: 5 weeks, 6 milestones** ✅

**Worth the extra week?** YES! SOLID is fundamental for senior engineers.

---

## 📚 Complete Curriculum (6 Milestones, 5 Weeks)

```
Week 1: Foundations (8-12 hours)
├── M0: Setup (1 evening, 1-2 hrs)
└── M1: Async News Fetcher (3-4 evenings, 6-8 hrs) → Checkpoint 1

Week 2: Software Design (8-10 hours) ⭐ ADDED BACK
└── M2: SOLID Refactoring (4-5 evenings, 8-10 hrs) → Checkpoint 2

Week 3: AI Agents (8-12 hours)
└── M3: First Agent with Tools (4-5 evenings, 8-10 hrs) → Checkpoint 3

Week 4: MCP & Multi-Agent (10-14 hours)
└── M4: MCP-Powered Pipeline (5-7 evenings, 10-14 hrs) → Checkpoint 4

Week 5: Quality (4-6 hours)
└── M5: Evaluation & Documentation (2-3 evenings, 4-6 hrs) → Checkpoint 5

Total: 5 weeks | 38-54 hours | 5 Checkpoints | 6 Milestones
```

---

## 📋 Detailed Milestone Breakdown

### Milestones 0-1: Same as v3.2
*(Setup and Async News Fetcher - see v3.2 for details)*

---

## ⭐ NEW: Milestone 2: SOLID Refactoring

**⏰ Time:** 4-5 evenings (8-10 hours)  
**When:** Week 2, Days 6-10  
**Checkpoint:** ✓ Checkpoint 2

### **Goal: Refactor Your Milestone 1 Code**
You built it quickly in Week 1. Now make it professional-grade!

---

#### Evening 6: Single Responsibility Principle (1.5-2 hrs)

**Concept:** One class = One responsibility

**Your Task: Analyze Current Code (30 min)**
- Review your fetchers
- Identify multiple responsibilities
- Make list of violations

**Provided for You:**
- ✅ SRP checklist
- ✅ Code smell guide
- ✅ Example analysis

**Refactor: Break Down Large Classes (60 min)**
```python
# BEFORE: Fetcher does too much
class HackerNewsFetcher:
    def fetch(self):
        data = self._fetch_from_api()
        data = self._transform_data(data)
        self._save_to_file(data)
        return data

# AFTER: Single responsibilities
class HackerNewsFetcher:
    def __init__(self, transformer, storage):
        self.transformer = transformer
        self.storage = storage
    
    def fetch(self):
        data = self._fetch_from_api()
        return data

class ArticleTransformer:
    def transform(self, data): ...

class MarkdownStorage:
    def save(self, articles): ...
```

**Your Refactor (guided):**
1. Extract data transformation → ArticleTransformer (20 min)
2. Extract file storage → MarkdownStorage (20 min)
3. Update tests (20 min)

**Skills:** SRP, code smell identification, extract class pattern

---

#### Evening 7: Open/Closed Principle (1.5-2 hrs)

**Concept:** Open for extension, closed for modification

**Your Task: Add GitHub Trending WITHOUT Modifying Existing Code**

**Read Pattern (20 min):**
- Factory pattern
- How to design for extension

**Create Abstract Base (30 min)** - **template provided**
```python
from abc import ABC, abstractmethod

class BaseFetcher(ABC):
    @abstractmethod
    async def fetch_articles(self) -> List[Article]:
        """Fetch articles from source."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return source name."""
        pass
```

**Refactor Existing Fetchers (30 min):**
1. Make HackerNews inherit from BaseFetcher
2. Make RSS inherit from BaseFetcher
3. Verify tests still pass

**Add GitHub Trending (30 min)** - **template provided**
```python
class GitHubTrendingFetcher(BaseFetcher):
    async def fetch_articles(self) -> List[Article]:
        # Implementation
        pass
    
    def get_source_name(self) -> str:
        return "github_trending"
```

**Register with Factory:**
```python
# No changes to existing classes needed!
orchestrator.register_fetcher(GitHubTrendingFetcher())
```

**Proof of OCP:** Added new functionality with ZERO changes to existing code! ✅

**Skills:** OCP, inheritance, abstract base classes, factory pattern

---

#### Evening 8: Liskov Substitution + Interface Segregation (2 hrs)

**Liskov Substitution Principle (60 min)**

**Concept:** Subclasses must be substitutable for base class

**Your Task: Verify Substitutability**

```python
# All fetchers should work identically
def test_fetcher_substitutability():
    fetchers = [
        HackerNewsFetcher(),
        RSSFetcher("https://example.com/feed"),
        GitHubTrendingFetcher()
    ]
    
    for fetcher in fetchers:
        # Should work for ANY fetcher
        articles = await fetcher.fetch_articles()
        assert isinstance(articles, list)
        assert all(isinstance(a, Article) for a in articles)
```

**Fix Violations (if any):**
- Ensure same return types
- Ensure same error handling
- Ensure same behavior contracts

**Interface Segregation Principle (60 min)**

**Concept:** Don't force classes to implement unused methods

**Your Task: Split Fat Interfaces**

**Before (Fat Interface):**
```python
class BaseFetcher(ABC):
    @abstractmethod
    async def fetch_articles(self): ...
    
    @abstractmethod
    async def fetch_with_pagination(self): ...  # Not all need this!
    
    @abstractmethod
    async def fetch_with_auth(self): ...  # Not all need this!
```

**After (Segregated):**
```python
class BaseFetcher(ABC):
    @abstractmethod
    async def fetch_articles(self): ...

class PaginatedFetcher(BaseFetcher):
    @abstractmethod
    async def fetch_page(self, page: int): ...

class AuthenticatedFetcher(BaseFetcher):
    @abstractmethod
    async def authenticate(self): ...
```

**Refactor your code** to use focused interfaces.

**Skills:** LSP, substitutability testing, ISP, interface design

---

#### Evening 9: Dependency Inversion Principle (1.5-2 hrs)

**Concept:** Depend on abstractions, not concrete classes

**Your Task: Inject Dependencies**

**Before (Tight Coupling):**
```python
class FetchOrchestrator:
    def __init__(self):
        # Depends on concrete classes!
        self.hn_fetcher = HackerNewsFetcher()
        self.rss_fetcher = RSSFetcher("https://...")
        self.storage = MarkdownStorage()
```

**After (Dependency Injection):**
```python
class FetchOrchestrator:
    def __init__(
        self,
        fetchers: List[BaseFetcher],
        storage: ArticleStorage
    ):
        # Depends on abstractions!
        self.fetchers = fetchers
        self.storage = storage

# Usage
orchestrator = FetchOrchestrator(
    fetchers=[
        HackerNewsFetcher(),
        RSSFetcher("https://..."),
        GitHubTrendingFetcher()
    ],
    storage=MarkdownStorage("data/articles")
)
```

**Your Refactor (60 min):**
1. Create ArticleStorage interface (20 min)
2. Update FetchOrchestrator (20 min)
3. Update tests with mocks (20 min)

**Benefits:**
- Easy to test (inject mocks)
- Easy to swap implementations
- Loose coupling

**Skills:** DIP, dependency injection, testability

---

#### Evening 10: Design Patterns & Cleanup (1.5-2 hrs)

**Apply Key Patterns (60 min)**

**1. Factory Pattern** (20 min)
```python
class FetcherFactory:
    @staticmethod
    def create_fetcher(source_type: str) -> BaseFetcher:
        if source_type == "hackernews":
            return HackerNewsFetcher()
        elif source_type == "rss":
            return RSSFetcher(config.rss_url)
        elif source_type == "github":
            return GitHubTrendingFetcher()
        raise ValueError(f"Unknown source: {source_type}")
```

**2. Strategy Pattern for Rate Limiting** (20 min)
```python
class RateLimitStrategy(ABC):
    @abstractmethod
    async def acquire(self): ...

class SemaphoreStrategy(RateLimitStrategy):
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def acquire(self):
        await self.semaphore.acquire()
```

**3. Template Method in BaseFetcher** (20 min)
```python
class BaseFetcher(ABC):
    async def fetch_articles(self) -> List[Article]:
        # Template method
        raw_data = await self._fetch_raw()
        articles = self._parse_data(raw_data)
        return self._filter_articles(articles)
    
    @abstractmethod
    async def _fetch_raw(self): ...
    
    @abstractmethod
    def _parse_data(self, data): ...
    
    def _filter_articles(self, articles):
        # Optional hook
        return articles
```

**Final Cleanup (30 min):**
1. Run all tests (10 min)
2. Fix any issues (15 min)
3. Code review checklist (5 min)

**Skills:** Factory pattern, Strategy pattern, Template Method pattern

---

#### Evening 11: Documentation & PR (1 hr)

**Document Design Decisions (30 min)**

Create `docs/design-decisions.md`:

```markdown
# Design Decisions

## Why Factory Pattern for Fetchers?
- **Problem:** Hard-coded fetcher instantiation
- **Solution:** Factory pattern for dynamic creation
- **Benefit:** Easy to add new sources via config

## Why Dependency Injection in Orchestrator?
- **Problem:** Tight coupling to concrete classes
- **Solution:** Constructor injection of abstractions
- **Benefit:** Testable, flexible, follows DIP

## Rate Limiting Strategy
- **Chose:** Strategy pattern
- **Alternatives:** Hard-coded semaphore
- **Rationale:** Different sources may need different limits
```

**Create PR (30 min):**
1. Write PR description highlighting SOLID improvements (15 min)
2. Include before/after code examples (10 min)
3. Submit for Checkpoint 2 review (5 min)

**PR Description Template:**
```markdown
## Milestone 2: SOLID Refactoring

### Changes
- Applied all 5 SOLID principles
- Added Factory, Strategy, Template Method patterns
- Refactored for extensibility and testability

### Proof of Open/Closed Principle
Added GitHub Trending source with ZERO changes to existing code.

### Testing
- All existing tests pass
- New tests for substitutability
- Mock-based tests using DI

### Design Patterns Applied
1. Factory Pattern - Fetcher creation
2. Strategy Pattern - Rate limiting
3. Template Method - BaseFetcher workflow
```

**Skills:** Technical writing, design documentation, PR creation

---

### Milestone 2 Deliverables

**Code Quality:**
- ✅ All 5 SOLID principles applied
- ✅ 3 design patterns implemented
- ✅ Dependency injection throughout
- ✅ Abstract base classes
- ✅ Factory for fetcher creation

**Extensibility Proof:**
- ✅ GitHub Trending added without modifying existing code
- ✅ Easy to add new sources
- ✅ Easy to swap rate limiting strategies

**Testing:**
- ✅ All tests still pass
- ✅ Substitutability tests added
- ✅ Mock-based tests using DI

**Documentation:**
- ✅ Design decisions documented
- ✅ Pattern rationale explained
- ✅ Architecture diagrams (optional but nice)

**Checkpoint 2 PR:** ✅ Ready for review

---

## 📊 Updated Time Breakdown

### **Week-by-Week Commitment:**

**Week 1: Foundations (8-12 hours)**
- M0: Setup (1 evening)
- M1: Async Fetcher (3-4 evenings)

**Week 2: Software Design (8-10 hours)** ⭐ NEW
- M2: SOLID Refactoring (4-5 evenings)

**Week 3: AI Agents (8-12 hours)**
- M3: First Agent with Tools (4-5 evenings)

**Week 4: MCP & Multi-Agent (10-14 hours)**
- M4: MCP-Powered Pipeline (5-7 evenings)

**Week 5: Quality (4-6 hours)**
- M5: Evaluation & Documentation (2-3 evenings)

**Total: 38-54 hours over 5 weeks**

---

## 🎓 Skills Breakdown

### **Total Skills Taught: 130+ skills**

| Milestone | Skills | Focus Area |
|-----------|--------|------------|
| M0: Setup | 5 | Project setup |
| M1: Fetcher | 12 | Async programming |
| **M2: SOLID** | **18** | **Software design** ⭐ |
| M3: Agent + Tools | 15 | AI agents |
| M4: MCP Pipeline | 25 | MCP + Multi-agent |
| M5: Evaluation | 8 | Quality & docs |

### **SOLID Milestone Skills (18 skills):**

**Principles (5):**
1. Single Responsibility Principle
2. Open/Closed Principle
3. Liskov Substitution Principle
4. Interface Segregation Principle
5. Dependency Inversion Principle

**Patterns (5):**
6. Factory Pattern
7. Strategy Pattern
8. Template Method Pattern
9. Dependency Injection
10. Abstract Base Classes

**Refactoring (4):**
11. Code smell identification
12. Extract class refactoring
13. Extract method refactoring
14. Interface design

**Testing (2):**
15. Substitutability testing
16. Mock-based testing

**Documentation (2):**
17. Design decision documentation
18. Technical writing

---

## 💡 Why SOLID Week Is Worth It

### **Career Impact:**

**Junior → Mid-Level:**
- SOLID principles expected
- Design patterns required
- Refactoring skills essential

**Without SOLID:**
- Can write code that works ✅
- Struggles with maintenance ❌
- Hard to extend systems ❌
- Poor testability ❌

**With SOLID:**
- Writes maintainable code ✅
- Easy to extend ✅
- Highly testable ✅
- Professional quality ✅

### **Real-World Value:**

**In Code Reviews:**
- "This violates SRP" → you know exactly what to fix
- "Depends on concrete class" → you apply DIP
- "Hard to test" → you use dependency injection

**In Architecture Discussions:**
- Can explain design decisions
- Can justify pattern choices
- Can debate trade-offs

**On Client Projects:**
- Build extensible systems
- Code is maintainable
- Team can work with your code

### **ROI Analysis:**

**Investment:** +1 week (8-10 hours)  
**Return:** 
- Professional-grade code skills
- Design pattern expertise
- Refactoring capability
- Interview advantage

**Worth It?** ✅ **Absolutely!**

---

## 🎯 Comparison: v3.2 vs v3.3

| Aspect | v3.2 (4 weeks) | v3.3 (5 weeks) ⭐ |
|--------|----------------|-------------------|
| **Total Hours** | 30-44 | 38-54 |
| **Duration** | 4 weeks | 5 weeks |
| **SOLID** | ❌ Skipped | ✅ Full week |
| **Design Patterns** | ⚠️ Taught inline | ✅ Applied deeply |
| **Refactoring** | ❌ No | ✅ Yes |
| **Code Quality** | ✅ Good | ✅ Professional |
| **Extensibility** | ⚠️ Basic | ✅ Proven |
| **Career Level** | Mid-level | Senior-ready |

---

## 🚀 Recommendation

### **Adopt v3.3 Self-Paced with SOLID** ✅

**Why:**

1. **SOLID is Fundamental**
   - Expected of senior engineers
   - Required for maintainable systems
   - Foundation for all design work

2. **Still Self-Paced Friendly**
   - 5 weeks is reasonable
   - 1-2 hours/evening maintained
   - Time-boxed tasks

3. **Better Career Outcomes**
   - More promotable engineers
   - Better code reviewers
   - Stronger architects

4. **Practical Learning**
   - Refactor your own code
   - See immediate benefits
   - Apply patterns hands-on

5. **Proves Concepts**
   - GitHub Trending with zero changes
   - Demonstrates Open/Closed
   - Validates learning

**Extra Week Investment:** ✅ Worth it for professional-grade engineers

---

## 📋 What Needs to Be Created

### **New for v3.3:**

1. **Milestone 2: SOLID Refactoring** (NEW)
   - 5 evening breakdowns
   - Code smell guides
   - Refactoring templates
   - Pattern examples
   - Before/after code
   - **Estimated:** 8-10 hours to create

2. **Updated Milestones 3-5**
   - Renumber from v3.2
   - Adjust references
   - **Estimated:** 2-3 hours

3. **Updated Rubrics**
   - Checkpoint 2: SOLID principles
   - Adjust checkpoint numbers
   - **Estimated:** 2-3 hours

4. **Additional Templates**
   - BaseFetcher template
   - Factory template
   - Strategy template
   - **Estimated:** 3-4 hours

**Total Creation Time: 15-20 hours**

---

## 📊 Final Summary

### **v3.3 Self-Paced Edition with SOLID**

**Structure:**
- 6 milestones (M0-M5)
- 5 weeks calendar time
- 38-54 total hours
- 5 PR checkpoints

**Key Features:**
- ✅ 1-2 hours per evening
- ✅ Full SOLID principles week
- ✅ MCP expertise
- ✅ Multi-agent systems
- ✅ Sustainable pace
- ✅ Professional-grade code

**Time Breakdown:**
- Week 1: Foundations (8-12 hrs)
- Week 2: SOLID (8-10 hrs) ⭐
- Week 3: AI Agents (8-12 hrs)
- Week 4: MCP (10-14 hrs)
- Week 5: Quality (4-6 hrs)

**What You Build:**
- Async news fetcher
- Refactored with SOLID
- AI agent with tools
- MCP server + pipeline
- Evaluation framework

**Career Outcome:**
- Production-ready
- Professional code quality
- Modern AI skills
- Design expertise

---

## ✅ Decision

**This is the right balance!**

- ✅ SOLID principles included (essential)
- ✅ Still self-paced friendly (1-2 hrs/evening)
- ✅ 5 weeks is reasonable
- ✅ Professional outcomes
- ✅ Modern AI skills

**Ready to create v3.3 materials?** 🚀

---

**Version:** 3.3 - Self-Paced Edition with SOLID  
**Time:** 1-2 hours/evening, 5 weeks  
**Total:** 38-54 hours  
**Status:** ✅ RECOMMENDED - Best balance of depth and pace
