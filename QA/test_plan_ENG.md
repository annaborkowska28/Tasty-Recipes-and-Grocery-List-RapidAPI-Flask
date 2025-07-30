# Test Plan – TastyAPI (EN)
## 1. Test Objective
The goal is to verify the functionality of the key features of the application:

- Recipe API endpoints
- Contact form validation
- Grocery list logic (add/remove/merge ingredients)
- Page navigation (About & Contact)
- Error handling and edge cases


## 2. Test Scope
- API testing using Postman (responses, structure, edge cases)
- UI validation of Contact form and navigation tabs
- Functionality testing of the shopping list feature
- Cross-browser checks (Chrome, Firefox)
- Responsiveness and accessibility via DevTools


## 3. Test Scenarios
### 3.1 API Tests (Postman)
- Verify successful response status: GET request - HTTP 200 OK
- Validate response structure: Fields such as title, image, ingredients, instructions must exist and not be empty
- Handle invalid requests: Non-existent recipe ID - HTTP 404 Not Found
- Confirm grocery list endpoints handle item merging and removal correctly
- Check edge cases (e.g. empty queries, incorrect data types)
- Data integrity:
    - Expected result: Fields title, image, description, ingredients, instructions are not empty
### 3.2 Navigation Tests 

- "About" tab redirects to /about
- "Contact" tab redirects to /contact
- Both tabs work properly on mobile and desktop screens

### 3.3 Contact Form Tests

- **Empty field submission:**
Attempting to submit the form with missing inputs (name, email, phone, or message) triggers appropriate error messages for each required field.
- **Valid submission:**
When all fields contain acceptable inputs (valid email format, sufficient message length, etc.), the form submits successfully and displays a confirmation message:
“Successfully sent your message!”
- **Invalid inputs and edge cases:**
  - Incorrect email format (missing @) -> “Please enter a valid email address”
  - Phone number includes letters or symbols -> validation error
  - Message field filled with only spaces -> rejected as invalid
  - Message length exceeds 1000 characters -> error message shown
  - Message with exactly 1000 characters -> submission is accepted
  - Message containing HTML tags -> neutralized and converted to plain text


### 3.4 Shopping List Functionality Tests

- Adding ingredients:

  - Add ingredients from a single recipe

  - Expected result: Ingredients appear in the shopping list

- Merging ingredients:

  - Add ingredients from multiple recipes

  - Expected result: Ingredients with the same name are summed

- Removing ingredients:

  - Remove an ingredient from the shopping list

  - Expected result: Ingredient is removed

- Empty list:

  - Remove all ingredients

  - Expected result: Message displayed ( "Your shopping list is empty")

## 4. Test Tools
- API testing - **Postman** (collections and environment) –

- UI and responsiveness - **Chrome browser + Devtools** 

- Test Management - **TestRail**
- Documentation - **Notion (custom QA database)**


## 5. Bug Reporting
Each bug should be reporte.g. API, contact form)

- Steps to reproduce the issue

- Expected result

- Actual result

- Attachments (screenshots), if possible