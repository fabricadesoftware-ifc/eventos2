<template>
  <b-menu :class="{ 'is-dark': dark }">
    <b-menu-list>
      <b-menu-item
        v-for="link in links"
        :key="link.title"
        tag="nuxt-link"
        exact-active-class="is-active"
        :to="localePath(link.to)"
      >
        <template v-slot:label>
          <b-icon v-if="link.icon" :icon="link.icon"></b-icon>
          <span>{{ link.title }}</span>
        </template>
      </b-menu-item>
    </b-menu-list>
  </b-menu>
</template>

<script>
/**
 * Menu de links.
 *
 * Cada objeto no prop `links` deve ter `title` e `to`.
 * Opcionalmente, pode conter um `icon`.
 */

export default {
  props: {
    links: {
      type: Array,
      default: () => []
    },
    dark: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss">
.is-dark {
  .menu-list a {
    display: flex;
    align-items: center;
    color: $white;

    .icon {
      margin-right: 6px;
    }

    &.is-active {
      color: darken($white, 20);
      background-color: inherit;
    }

    &:hover {
      background-color: $primary;
    }
  }
}
</style>
