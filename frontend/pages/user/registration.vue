<template>
  <div class="container">
    <div class="columns is-gapless is-centered">
      <div class="column is-8">
        <main class="section">
          <h1 class="title">{{ $t('pages.user-registration.title') }}</h1>

          <div v-if="eventRegistration">
            {{ $t('pages.user-registration.hasRegistration') }}
          </div>
          <div v-else>
            {{ $t('pages.user-registration.hasNoRegistration') }}
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['eventRegistration'])
  }
}
</script>
