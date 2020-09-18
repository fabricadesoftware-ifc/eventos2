<template>
  <div class="user-search">
    <div class="panel">
      <div class="panel-heading">
        {{ $t('components.userSearch.heading') }}
      </div>
      <div class="panel-block">
        <div class="control">
          <b-field>
            <b-input
              v-model="searchInput"
              expanded
              @keydown.native.enter="search"
            ></b-input>
            <div class="control">
              <b-button type="is-primary" @click="search">{{
                $t('components.userSearch.searchButton')
              }}</b-button>
            </div>
          </b-field>
        </div>
      </div>
      <template v-if="users.length">
        <a v-for="user in users" :key="user.public_id" class="panel-block user">
          <b-icon icon="account" class="panel-icon" />
          <div class="control">
            {{ user.first_name + ' ' + user.last_name }}
          </div>
          <div class="control">
            <b-button
              icon-left="plus"
              class="is-pulled-right"
              size="is-small"
              @click="addUser(user)"
              >{{ $t('components.userSearch.addButton') }}</b-button
            >
          </div>
        </a>
      </template>
      <template v-else-if="dirty">
        <div class="panel-block">
          {{ $t('components.userSearch.noResults') }}
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dirty: false,
      searchInput: '',
      users: []
    }
  },
  methods: {
    search() {
      if (!this.searchInput) {
        this.users = []
        return
      }
      this.dirty = true
      this.$api.user
        .list({ email: this.searchInput })
        .then(users => (this.users = users))
    },
    reset() {
      this.users = []
      this.searchInput = ''
      this.dirty = false
    },
    addUser(user) {
      this.$emit('select', user)
      this.reset()
    }
  }
}
</script>
