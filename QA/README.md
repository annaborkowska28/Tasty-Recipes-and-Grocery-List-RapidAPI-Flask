# QA Folder – TastyAPI Testing

This folder contains files related to API testing for the TastyAPI project. 

It shows how the app has been verified through test cases, Postman requests, and documentation.

Screenshots from TestRail — including executed test runs and mapped test cases — can be found in the `docs` folder

## Contents

- `TASTY.postman_collection.json` – Collection with requests for testing all major API endpoints
- `tasty-local.postman_environment.json` – Local Postman environment for testing on `localhost`
- `testrail_to_postman.md` – Document showing which TestRail cases map to Postman requests
- Test Cases Databasae in Notion - https://www.notion.so/TASTY-API-Manual-Test-Cases-231bedf2cbf8806aa649e4d08cc7a818?source=copy_link

## How to Use

1. Open Postman
2. Import the collection and environment files from this folder
3. **Make sure the TastyAPI app is running locally at** `http://localhost:5000`
4. Use the environment to run requests
5. Check `testrail_to_postman.md` to see test coverage and status

> **Note:** This API must be running locally for Postman tests to work.  
> These files are included to showcase tested endpoints and expected behavior.

## What's Covered

- Grocery list logic (add, remove, merge ingredients)
- Recipe search and detail view
- Contact form validation (email, phone, message length)
- Edge case handling and input errors

## Notes

- Navigation links (menu/footer) are not tested in Postman
- External links (GitHub, Facebook, Twitter) are verified manually
