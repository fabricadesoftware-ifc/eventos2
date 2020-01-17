<template>
  <div class="container">
    <div class="columns">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ eventName }}</h1>
          <p>
            {{ eventStartDate.format('LLL') }}
            &ndash;
            {{ eventEndDate.format('LLL') }}
          </p>
          <b-button type="is-primary">
            {{ $t('pages.index.registerButton') }}
          </b-button>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

/**
 * Página inicial de um evento.
 */
export default {
  auth: false,
  computed: {
    ...mapGetters(['eventName', 'eventStartDate', 'eventEndDate'])
  }
}
</script>
