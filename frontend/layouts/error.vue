<template>
  <div>
    <eventos-navbar />

    <div class="container">
      <div class="columns is-gapless is-centered">
        <div class="column is-10">
          <main class="section">
            <div class="error-oops">
              {{ headerMessage }}
            </div>
            <div v-if="statusCode" class="error-status-code">
              {{ statusCode }}
            </div>
            <div class="error-message">{{ message }}</div>
            <b-button
              v-if="event"
              icon-left="home"
              type="is-primary"
              size="is-medium"
              @click="goHome"
              >{{ $t('pages.error.goHomeButton') }}</b-button
            >
            <div v-else class="error-advice">
              {{ $t('pages.error.adviceEventNotFound') }}
            </div>
          </main>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import EventosNavbar from '~/components/EventosNavbar'

export default {
  name: 'NuxtError',
  components: {
    EventosNavbar
  },
  layout: 'blank',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  head() {
    return {
      title: this.message
    }
  },
  computed: {
    ...mapState(['event']),
    headerMessage() {
      const message = this.hasEvent ? 'header' : 'headerEventNotFound'
      return this.$t(`pages.error.${message}`)
    },
    message() {
      let message = this.error.message
      if (!message.endsWith('.')) {
        message += '.'
      }
      return message
    },
    statusCode() {
      return this.error.statusCode
    }
  },
  methods: {
    goHome() {
      this.$router.go(this.localePath({ name: 'index' }))
    }
  }
}
</script>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.error-oops {
  margin-bottom: 2.1em;
  font-size: 1.3em;
  border-bottom: 3px solid $warning;
}
.error-status-code {
  font-size: 1.5em;
  font-weight: bold;
  line-height: 0.9;
}
.error-message {
  margin-bottom: 3em;
  font-size: 1.7em;
  font-family: monospace;
}
.error-advice {
  font-size: 1.3em;
}
</style>
