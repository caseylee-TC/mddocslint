// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeAstroRelativeMarkdownLinks from 'astro-rehype-relative-markdown-links';

const base = '/mddocslint';

// https://astro.build/config
export default defineConfig({
	site: 'https://caseylee-tc.github.io',
	base,
	markdown: {
		// Rewrite relative .md links (./usage.md) to site URLs (/mddocslint/usage/).
		rehypePlugins: [
			[
				rehypeAstroRelativeMarkdownLinks,
				// Starlight serves the docs collection at the site root, with trailing slashes.
				{ base, collectionBase: false, trailingSlash: 'always' },
			],
		],
	},
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
