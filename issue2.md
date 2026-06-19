## Problem
The reusable `Modal` component currently provides basic functionality (backdrop click, Escape key handling, body scroll locking), but it does not fully support accessibility best practices.

Current limitations:
* Missing `role="dialog"`
* Missing `aria-modal="true"`
* No focus trapping while the modal is open
* Focus is not automatically moved into the modal when opened
* Focus is not restored to the previously focused element when closed

This can make keyboard navigation difficult and may reduce compatibility with assistive technologies.

## Proposed Solution
Enhance `frontend/components/Modal.tsx` with accessibility improvements:
* Add `role="dialog"`
* Add `aria-modal="true"`
* Associate the modal title using `aria-labelledby`
* Automatically focus the modal or first interactive element when opened
* Trap focus within the modal while it remains open
* Restore focus to the previously focused element when the modal closes

## Benefits
* Better keyboard accessibility
* Improved screen reader support
* Reusable accessible modal pattern for future dialogs
* Alignment with common accessibility standards and React UI best practices

## Acceptance Criteria
* Modal includes proper ARIA attributes
* Keyboard users cannot tab outside the modal while open
* Focus moves into the modal on open
* Focus returns to the triggering element on close
* Existing rollback confirmation flow continues to work correctly
