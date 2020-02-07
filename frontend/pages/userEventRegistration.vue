<template>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-8">
        <main class="section">
          <h1 class="title">{{ $t('pages.userEventRegistration.title') }}</h1>

          <div v-if="eventUserRegistration" class="card">
            <div class="card-content">
              {{ eventUserRegistration.registration_type.name }}
            </div>
          </div>
          <div v-else>
            {{ $t('pages.userEventRegistration.noRegistration') }}
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['eventUserRegistration'])
  }
}
</script>
