<template>
  <div id="app">
    <month-picker-input lang="ru" @input="showDateFrom"></month-picker-input>
    <month-picker-input lang="ru" @input="showDateTo"></month-picker-input>
    <button @click="recount">Получить обновленные данные</button>
    <select v-model="params" >
      <option value="stoim">Стоимость</option>
      <option value="netto">Вес</option>
    </select>
    <select v-model="interval">
      <option value="year">Год</option>
      <option value="quartal">Квартал</option>
      <option value="month">Месяц</option>
    </select>
    <market-summary ref="marketSummary" :date="date"></market-summary>
    <exp-imp-dynamics ref="expImpDynamics"
                      :date="date"
                      :params="params"
                      :interval="interval"
    ></exp-imp-dynamics>
  </div>
</template>

<script>
  import { MonthPickerInput } from 'vue-month-picker'




export default {
  name: 'app',
  components: {
    MonthPickerInput,
    MarketSummary: () => import('./components/MarketSummary'),
    ExpImpDynamics: () => import('./components/ExpImpDynamics')
  },
  data() {
    return {
      date: {
        from: null,
        to: null

      },
      params: 'stoim',
      interval: 'year'
    }
  },
  methods: {
    recount () {
      this.$refs.marketSummary.recount();
      this.$refs.expImpDynamics.recount();
    },
    showDateFrom (date) {

      if (date.monthIndex.toString().length === 1) {
        this.date.from = `${date.year}-0${date.monthIndex}`
      } else {
        this.date.from = `${date.year}-${date.monthIndex}`
      }
    },
    showDateTo (date) {
      if (date.monthIndex.toString().length === 1) {
        this.date.to = `${date.year}-0${date.monthIndex}`
      } else {
        this.date.to = `${date.year}-${date.monthIndex}`
      }
    }
  },
  mounted() {
    Date
  }

}
</script>

<style>
.month-picker__container {
  z-index: 100;
}
.month-picker__year p {
  background: #ffffff;
  margin-block-start: 0px !important;
  margin-block-end: 0px !important;
  padding-bottom: 1em;
  padding-top: 1em;
}
</style>
