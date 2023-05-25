export const versionInfo = (() => {
  try {
    return require('../../git-version.json');
  } catch {
    // In dev the file might not exist:
    return { hash: 'dev' };
  }
})();
