<template>
  <div>
    <h2>The fruit of the day is {{ fruit.name }}</h2>
    <h4>And the time is {{ fruit.date }}</h4>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'FruitClock',
  data () {
    return {
      /**
       * This prevents an error when UI tries to access `fruit` before it was created.
       */
      fruit: {}
    }
  },
  mounted () {
    const self = this
    this.$apollo.subscribe({
      query: gql`subscription {
        fruit {
          name
          date
        }
      }`,
      variables: {}
    }).subscribe({
      next (payload) {
        self.fruit = payload.data.fruit
      },
      error (err) {
        console.err(err)
      }
    })
  }
  // apollo: {
  //   fruit: gql`query {
  //     fruit {
  //       name
  //       date
  //     }
  //   }`
  // }
}
</script>
