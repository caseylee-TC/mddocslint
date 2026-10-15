// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'mddocslint',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/caseylee-TC/mddocslint' }],
			sidebar: [
				{ label: 'Home', slug: '' },
				{ label: 'Install', slug: 'install' },
				{ label: 'Usage', slug: 'usage' },
				{ label: 'Rules reference', slug: 'rules' },
				{ label: 'Case study', slug: 'case-study' },
			],
		}),
	],
});
