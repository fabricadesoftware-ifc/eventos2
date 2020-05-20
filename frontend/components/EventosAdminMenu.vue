<template>
  <section class="admin-menu">
    <h1 class="title is-5">{{ $t('adminMenu.title') }}</h1>
    <b-menu>
      <b-menu-list :label="$t('adminMenu.overview')">
        <b-menu-item
          :label="$t('pages.admin.title')"
          tag="nuxt-link"
          :to="localePath({ name: 'admin' })"
          exact-active-class="is-active"
        />
        <b-menu-item
          :label="$t('pages.admin-registrations.title')"
          tag="nuxt-link"
          :to="localePath({ name: 'admin-registrations' })"
          active-class="is-active"
        />
      </b-menu-list>
      <b-menu-list :label="$t('adminMenu.configuration')">
        <b-menu-item
          :label="$t('pages.admin-eventDetails.title')"
          tag="nuxt-link"
          :to="localePath({ name: 'admin-eventDetails' })"
          active-class="is-active"
        />
      </b-menu-list>
      <b-menu-list :label="$t('adminMenu.activities')">
        <b-menu-item
          :label="$t('pages.admin-activities.title')"
          tag="nuxt-link"
          :to="localePath({ name: 'admin-activities' })"
          active-class="is-active"
        />
      </b-menu-list>
    </b-menu>
  </section>
</template>

<script>
export default {}
</script>

<style lang="scss">
.admin-menu {
  padding: 1.5em 1.5em 2em 2em;
  .menu-list li a {
    padding-right: 4em;
    border-radius: 0;
  }
}
</style>
