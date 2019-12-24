<template>
  <div class="app">
    <month-picker-input @input="date_from" :no-default="true" lang="ru"></month-picker-input>
    <month-picker-input @input='date_to' :no-default="true" lang="ru"></month-picker-input>
    <select v-model="params">
      <option value="stoim">Стоимость</option>
      <option value="netto">Нетто</option>
    </select>
    <select v-model="category">
      <option value="IM">Импорт</option>
      <option value="EX">Экспорт</option>
    </select>
    <select v-model="interval">
      <option value="year">Год</option>
      <option value="quartal">Квартал</option>
      <option value="month">Месяц</option>
    </select>
    <button @click="getData">Получить обновленные данные</button>
    <market-summary :date="date" ref="marketSummary"></market-summary>
    <exp-imp-dynamics :date="date"
                      :params="params"
                      :interval="interval"
                      ref="expImpDynamics"
    ></exp-imp-dynamics>
    <turnover-structure
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            ref="turnoverStructure"
    ></turnover-structure>
  </div>
</template>


<script>

import { MonthPickerInput } from 'vue-month-picker'

export default {
  name: 'App',
  data() {
      return {
          date: {
              from: null,
              to: null
          },
          params: 'stoim',
          interval: 'year',
          category: 'IM',
      }
  },
  methods: {
      getData() {
          this.$refs.marketSummary.recount();
          this.$refs.expImpDynamics.recount();
          this.$refs.turnoverStructure.clear();
          this.$refs.turnoverStructure.recount();
      },
      date_from(data) {
          if (String(data.monthIndex).length === 1) {
              this.date.from = data.year + '-' + '0' + data.monthIndex
          } else {
              this.date.from = data.year + '-' + data.monthIndex
          }
      },
      date_to(data) {
          if (String(data.monthIndex).length === 1) {
              this.date.to = data.year + '-' + '0' + data.monthIndex
          } else {
              this.date.to = data.year + '-' + data.monthIndex
          }
      }
  },
  components: {
    MonthPickerInput,
    MarketSummary: () => import('./components/MarketSummary'),
    ExpImpDynamics: () => import('./components/ExpImpDynamics'),
    TurnoverStructure: () => import('./components/TurnoverStructure')
  },
};
</script>


<style>
    .month-picker__container {
        z-index: 100;
    }
    .month-picker__year p {
        background-color: white;
        margin-block-start: 0 !important;
        margin-block-end: 0 !important;
        padding-top: 1em;
        padding-bottom: 1em;
    }
</style>