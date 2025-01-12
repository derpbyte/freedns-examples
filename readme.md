## "A Python API wrapper for FreeDNS.afraid.org" with additional examples

A fork of the original FreeDNS API wrapper repo with more examples:

`examples/cli`: Working example of the FreeDNS API Wrapper as a CLI tool. Lets you:

- Login
- Create Subdomains
- Sign up
- ~~Captchas auto-solved using `captcha-solver` (API key required)~~

`examples/server`: Working example of the API Wrapper as a simple web-interface.

- Lets you do all of `examples/cli`
- Captcha images are rendered on the server and shown as an `<img>`, must be manually solved
- Made for single-user scenarios only, as the server requests a single captcha at a time