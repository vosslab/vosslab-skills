/**
 * Voss Lab Skills plugin for OpenCode.ai
 *
 * Auto-registers skills directory via config hook.
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const VosslabSkillsPlugin = async ({ client, directory }) => {
  // resolve skills directory relative to this plugin file
  const skillsDir = path.resolve(__dirname, '../../skills');

  return {
    // inject skills path into live config so OpenCode discovers all skills
    // without requiring manual symlinks or config file edits
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }
    },
  };
};
