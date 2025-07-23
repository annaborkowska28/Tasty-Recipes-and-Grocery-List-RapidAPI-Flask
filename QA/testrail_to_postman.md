# TestRail – Postman Mapping

This document maps manual test cases from TestRail to API requests created in Postman.  
It shows which scenarios are covered by automated API tests and which require manual or UI testing.

---

## Limitations

- Navigation elements (header/footer) are not tested via Postman  
- External links (e.g. GitHub, Facebook, Twitter) are excluded from API testing  
- UI layout, rendering, and interactions are outside the scope of Postman tests

---

## Navigation

| Test Case ID | Description                      | Postman Request        | Coverage    |
|--------------|----------------------------------|------------------------|-------------|
| C1           | “Contact” tab navigation         | Not directly tested    | Partial     |
| C2           | “About” tab navigation           | Not directly tested    | Not covered |
| C3           | Homepage link “Recipes by Tasty” | GET /                  | Covered     |
| C4           | “Grocery List” tab navigation    | GET /view-grocery-list | Covered     |

---

## Footer Navigation

| Test Case ID | Description             | Postman Request | Coverage    |
|--------------|-------------------------|-----------------|-------------|
| C5           | GitHub link in footer   | Not applicable  | Not covered |
| C6           | Facebook link in footer | Not applicable  | Not covered |
| C7           | Twitter link in footer  | Not applicable  | Not covered |

> **Note:** Footer links are verified manually.

---

##  Contact Form

| Test Case ID | Description                                | Postman Request | Coverage |
|--------------|--------------------------------------------|-----------------|----------|
| C8           | Valid contact form submission              | POST /contact   | Covered  |
| C9           | Submit empty contact form                  | POST /contact   | Covered  |
| C10          | Submit form with invalid email             | POST /contact   | Covered  |
| C11          | Phone number includes letters              | POST /contact   | Covered  |
| C12          | Message field with only spaces             | POST /contact   | Covered  |
| C13          | Message field exceeds 1000 characters      | POST /contact   | Covered  |
| C14          | Message field with exactly 1000 characters | POST /contact   | Covered  |
| C15          | Message field with HTML tag injection      | POST /contact   | Covered  |

---

## Grocery List

| Test Case ID | Description                              | Postman Request                | Coverage |
|--------------|------------------------------------------|--------------------------------|----------|
| C16          | Add ingredients to grocery list          | POST /add-to-grocery-list/<id> | Covered  |
| C17          | Merge ingredients from multiple recipes  | POST /add-to-grocery-list/<id> | Covered  |
| C18          | Remove a single ingredient from the list | POST /remove-from-grocery-list | Covered  |
| C19          | Clear the entire grocery list            | POST /clear-grocery-list       | Covered  |

---

## Legend

- **Covered** – Request exists in Postman and has been tested  
- **Partial** – Feature is indirectly covered or incomplete  
- **Not implemented yet** – Request not yet added to Postman collection