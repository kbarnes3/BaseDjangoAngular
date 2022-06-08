export const versionInfo = (() => {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require('../../git-version.json');
  } catch {
    // In dev the file might not exist:
    return { hash: 'dev' };
  }
})();
