# Virtual Assistant Chat

A Svelte-based chat application featuring a virtual assistant interface.

## Project Overview

This project is built using the Svelte framework and utilizes various libraries such as GSAP for animations and Lucide Svelte for icons. The application provides a chat interface integrating both user and assistant avatars along with message interaction capabilities.

## Requirements

- Node.js 20.x

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/your-username/virtual-assistant-chat.git
  ```

2. Navigate to the project directory:

  ```bash
  cd virtual-assistant-chat
  ```

3. Install dependencies:

  ```bash
  npm install
  ```

## Development

To start a development server:

```bash
npm run dev
```

This will start the Vite development server, and you can view your application by visiting `http://localhost:your-port` in your browser.

## Building

To create a production version of your app:

```bash
npm run build
```

The output will be in the `dist` directory. You can preview it using:

```bash
npm run preview
```

## Testing

Run the unit tests with:

```bash
npm run test
```

To watch tests for changes:

```bash
npm run test:unit -- --watch
```

## Linting and Formatting

Check and format your code using:

```bash
npm run lint
npm run format
```

## Releasing

Whenever a tag is pushed a new release is created an the package is
published to the NPM registry using GitHub Actions.

Bump the current version using `npm` as follows:

```sh
# for versions with breaking changes use `major`
npm version major

# for versions with non-breaking changes use `minor`
npm version minor

# for patch versions use `patch`
npm version patch
```

Then push the repository including tag metadata as follows

```sh
git push origin main --follow-tags
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
