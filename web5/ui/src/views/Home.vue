<template>
  <div class="home">
    <h2>The fruit of the day is {{ fruit }}</h2>
    <h4>And the time is {{ time }}</h4>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      fruit: '',
      time: ''
    }
  }
}
</script>
