# The application's own CSP makes Playwright's `wait_for_function` unusable

- **Discovered:** 2026-09-18
- **Review by:** 2027-03-18
- **Source:** measured on this repository, 2026-09-18 — `page.wait_for_function`
  in `tests/e2e/test_larger_view_browser.py` against the running application
- **Affects:** `tests/e2e/**`, `src/mygallery/app.py` (`SECURITY_HEADERS`)

## The constraint

Slice 1 set `Content-Security-Policy: default-src 'self'` on every response.
That policy forbids `unsafe-eval`, and **`page.wait_for_function` evaluates its
predicate as a string inside the page**, so every call fails:

```
playwright._impl._errors.Error: Page.wait_for_function: EvalError:
Evaluating a string as JavaScript violates the following Content Security
Policy directive because 'unsafe-eval' is not an allowed source of script:
default-src 'self'".
    at eval (<anonymous>)
    at predicate (eval at evaluate (:311:30), <anonymous>:4:60)
```

It is not a flake, a timing problem or a bad selector, which is what the error
looks like at first glance — the stack points into Playwright's own generated
code rather than at anything in the test.

**`page.evaluate` is unaffected.** It runs through the Chrome DevTools Protocol
rather than in-page `eval`, so the page's CSP does not apply to it. So does
Playwright's `expect(...)` auto-waiting, which polls through the same channel.
The distinction is invisible from the test's side and is the whole of this
constraint: two APIs that look equivalent behave differently under our own
security header.

## How we know

Reproduce by calling `page.wait_for_function("window.scrollY > 0")` in any test
against the running application. Observed while writing the scroll-position
test for `REQ-GAL-004`.

The CSP itself is asserted by `tests/test_app.py::test_the_gallery_page_is_served_with_a_content_security_policy`,
so this will hold as long as that test does.

## What we do about it

**In place now:** belt-B tests use `page.evaluate` for anything they need to
read or set in the page, and Playwright's `expect(...)` for anything they need
to wait for. Neither touches in-page `eval`. `tests/e2e/test_larger_view_browser.py`
carries a comment at the one place it mattered.

**Do not resolve this by adding `'unsafe-eval'` to the Content-Security-Policy.**
That would weaken a production security header — one that
`rules/javascript/security.md` calls the control that limits the damage when
something else is missed — purely to make a test convenient. The test has an
equivalent that works.

If a future test genuinely needs to poll a condition that `expect(...)` cannot
express, poll it from the test side with `page.evaluate` in a loop rather than
handing a predicate to the page.
