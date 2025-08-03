import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'doc',
      id: 'README',
      label: 'Data Synchronization',
    },
    {
      type: 'doc',
      id: 'sync-client',
      label: 'Sync Client',
    },
    {
      type: 'category',
      label: 'Sync Server',
      link: {
        type: 'doc',
        id: 'sync-server/README',
      },
      items: [
        {
          type: 'doc',
          id: 'sync-server/configuration',
          label: 'Configuration',
        },
        {
          type: 'doc',
          id: 'sync-server/jwt-authentication',
          label: 'JWT Authentication',
        },
        {
          type: 'doc',
          id: 'sync-server/sync-cluster',
          label: 'Sync Cluster',
        },
        {
          type: 'doc',
          id: 'sync-server/embedded-sync-server',
          label: 'Embedded Sync Server',
        },
        {
          type: 'category',
          label: 'GraphQL',
          link: {
            type: 'doc',
            id: 'sync-server/graphql-database/README',
          },
          items: [
            {
              type: 'doc',
              id: 'sync-server/graphql-database/graphql-queries',
              label: 'GraphQL Queries',
            },
            {
              type: 'doc',
              id: 'sync-server/graphql-database/graphql-mutations',
              label: 'GraphQL Mutations',
            },
            {
              type: 'doc',
              id: 'sync-server/graphql-database/graphql-python-client',
              label: 'GraphQL Python Client',
            },
          ],
        },
        {
          type: 'doc',
          id: 'sync-server/changelog',
          label: 'Changelog',
        },
      ],
    },
    {
      type: 'category',
      label: 'Data Model',
      link: {
        type: 'doc',
        id: 'data-model/README',
      },
      items: [
        {
          type: 'doc',
          id: 'data-model/object-ids',
          label: 'Object IDs and Sync',
        },
      ],
    },
    {
      type: 'category',
      label: 'MongoDB Sync Connector',
      link: {
        type: 'doc',
        id: 'mongodb-sync-connector/README',
      },
      items: [
        {
          type: 'doc',
          id: 'mongodb-sync-connector/mongodb-configuration',
          label: 'MongoDB Configuration',
        },
        {
          type: 'doc',
          id: 'mongodb-sync-connector/objectbox-sync-connector-setup',
          label: 'ObjectBox Sync Connector Setup',
        },
        {
          type: 'doc',
          id: 'mongodb-sync-connector/mongodb-data-mapping',
          label: 'MongoDB Data Mapping',
        },
      ],
    },
    {
      type: 'doc',
      id: 'troubleshooting-sync',
      label: 'Troubleshooting Sync',
    },
    {
      type: 'doc',
      id: 'faq',
      label: 'FAQ',
    },
    // Separator for external links section
    {
      type: 'html',
      value: '<hr style="margin: 1rem 0; border: none; border-top: 1px solid #d1d5db;" />',
    },
    {
      type: 'category',
      label: 'OBJECTBOX DATABASE DEVELOPER DOCS',
      collapsible: false,
      items: [
        {
          type: 'link',
          label: 'Java, Kotlin, Flutter/Dart',
          href: 'https://docs.objectbox.io/',
        },
        {
          type: 'link',
          label: 'C, C++',
          href: 'https://cpp.objectbox.io/',
        },
        {
          type: 'link',
          label: 'Swift',
          href: 'https://swift.objectbox.io/',
        },
        {
          type: 'link',
          label: 'Go',
          href: 'https://golang.objectbox.io/',
        },
      ],
    },
  ],
};

export default sidebars;
