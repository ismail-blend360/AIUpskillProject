# Design Decisions - Milestone 2 Refactoring

## Summary

Refactored Milestone 1 codebase to follow SOLID principles and design patterns.

## Changes Made

### 1. Single Responsibility Principle

**Problem:** Fetchers had multiple responsibilities (fetch, transform, save)

**Solution:**
- Extracted `ArticleTransformer` class (responsibility: transform data)
- Extracted `MarkdownStorage` class (responsibility: save to files)
- Fetchers now only fetch (single responsibility)

**Benefit:** Changes to transformation logic don't affect fetchers

### 2. Open/Closed Principle

**Problem:** Adding new source required modifying existing code

**Solution:**
- Created `BaseFetcher` abstract base class
- All fetchers inherit from BaseFetcher
- New sources extend without modifying existing

**Proof:** Added GitHub Trending with ZERO changes to existing code

**Benefit:** New sources can be added safely, no regression risk

### 3. Liskov Substitution Principle

**Problem:** Fetchers had inconsistent interfaces

**Solution:**
- Defined clear contract in BaseFetcher
- All fetchers implement same interface
- Substitutability tests ensure compliance

**Benefit:** Any fetcher can be used anywhere BaseFetcher is expected

### 4. Interface Segregation Principle

**Problem:** Risk of fat interfaces forcing unused methods

**Solution:**
- BaseFetcher has minimal interface (3 methods)
- Optional interfaces for special cases (AuthenticatedFetcher, etc.)
- Fetchers only implement what they need

**Benefit:** Clean, focused interfaces

### 5. Dependency Inversion Principle

**Problem:** Classes depended on concrete implementations

**Solution:**
- Created `ArticleStorage` interface
- Dependencies injected via constructors
- Code depends on abstractions

**Benefit:** Easy to test (inject mocks), easy to swap implementations

## Design Patterns Applied

### Factory Pattern

**Location:** `src/factories/fetcher_factory.py`

**Purpose:** Create fetchers without knowing concrete classes

**Usage:**
```python
fetcher = FetcherFactory.create('hackernews', transformer, storage)