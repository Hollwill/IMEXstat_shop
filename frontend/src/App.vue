<template>
  <div class="app">
    <div class="sidenav">
      <p><router-link :to="{name: 'market_summary'}">Сводка рынка</router-link></p>
      <p><router-link :to="{name: 'report_tnved'}">Отчет по ТНВЭД</router-link></p>
      <p><router-link :to="{name: 'report_country'}">Отчет по странам</router-link></p>
      <p><router-link :to="{name: 'report_region'}">Отчет по регионам</router-link></p>
    </div>
    <div class="main">
      <div class="data-pickers">
        <month-picker-input @input="date_from" :no-default="true" lang="ru"></month-picker-input>
        <month-picker-input @input='date_to' :no-default="true" lang="ru"></month-picker-input>
      </div>
<!--      <input type="text" v-model="item">-->
      <autocomplete :min-len="2" @item-clicked="tnved_search" :placeholder="'Введите код тнвэд'" :items="items" v-model="item" :get-label="getLabel" :component-item="template" @update-items="updateItems"></autocomplete>
      <button @click="addItem">+</button>
      <div class="item_list" v-for="(tnved, index) in selectedTnved" :key="index">
        <span class="div-as-button" @click="rmItem(index, selectedTnved)">{{tnved}}</span>
      </div>
      <div class="item_list" v-for="(country, index) in selectedCountry" :key="index">
        <span class="div-as-button" @click="rmItem(index, selectedCountry)">{{country}}</span>
      </div>
      <div class="item_list" v-for="(region, index) in selectedRegion" :key="index">
        <span class="div-as-button" @click="rmItem(index, selectedRegion)">{{region}}</span>
      </div>

      <br>
      <select v-model="params">
        <option value="stoim">Стоимость</option>
        <option value="netto">Нетто</option>
      </select>
      <select v-model="category">
        <option value="ИМ">Импорт</option>
        <option value="ЭК">Экспорт</option>
      </select>
      <select v-model="interval">
        <option value="year">Год</option>
        <option value="quartal">Квартал</option>
        <option value="month">Месяц</option>
      </select>
      <button @click="getData">Получить обновленные данные</button>
    </div>
    <div id="page-container">
      <router-view
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :tnved_list="selectedItems"
        ></router-view>
    </div>
  </div>
</template>


<script>
import { MonthPickerInput } from 'vue-month-picker'
import Autocomplete from 'v-autocomplete'
import 'v-autocomplete/dist/v-autocomplete.css'
import AutocompleteItemTemplate from "./AutocompleteItemTemplate";
import {HTTP} from './http-common'

export default {
  name: 'App',
  data() {
      return {
          template: AutocompleteItemTemplate,
          items: [],
          item: null,
          selectedTnved: [],
          selectedCountry: [],
          selectedRegion: [],
          date: {
              from: null,
              to: null
          },
          params: 'stoim',
          interval: 'year',
          category: 'ИМ',
      }
  },
  computed: {
    // eslint-disable-next-line vue/return-in-computed-property
    selectedItems: function() {
        if (this.$route.name === 'report_tnved') {
          return this.selectedTnved
        } else if (this.$route.name === 'report_country') {
          return this.selectedCountry
        } else if (this.$route.name === 'report_region') {
          return this.selectedRegion
        }
      },
  },
  methods: {

      tnved_search() {
        if (this.$route.name === 'report_tnved' && this.item.length < 10) {
          this.updateItems(this.item)
        }
      },
      addItem () {
        if (this.item) {
          if (this.$route.name === 'report_tnved') {
            this.selectedTnved.push(this.item);
          } else if (this.$route.name === 'report_country') {
            this.selectedCountry.push(this.item);
          } else if (this.$route.name === 'report_region') {
            this.selectedRegion.push(this.item)
          }
          this.item = null
        }
      },
      rmItem (index, list) {
          list.splice(index, 1)
      },
      updateItems (text) {
        if (text) {
          let category
          if (this.$route.name === 'report_tnved' && text.length % 2 === 0) {
            category = 'tnved'
          } else if (this.$route.name === 'report_country') {
            category = 'country'
          } else if (this.$route.name === 'report_region') {
            category = 'region'
          }
          HTTP.get('statistic/autocomplete/', {
              params: {
                  'q': text,
                  'category': category
              }
          })
              .then(response => {
                  this.items = response.data

              })
        }
      },
      getLabel(item) {
          return item
      },
      getData() {
          this.$eventHub.$emit('recount')
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
    Autocomplete
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
    .sidenav {
      width: 160px;
      z-index: 1;
      top: 0;
      left: 0;
      background-color: #111;
      overflow-x: hidden;
      padding-top: 20px;
      margin-right: 0;
    }
    .main {
      margin-left: 160px; /* Same as the width of the sidenav */
      padding: 0px 10px;
    }
    .router-link-active {
      color: orange;
    }
    .data-pickers {
      margin: 0 !important;
    }
  *{
    box-sizing: border-box;
  }
  .d-table{
    display: table;
    width: 100%;
    border-collapse: collapse;
  }
  .d-tr{
    display: table-row;
  }
  .d-td{
    display: table-cell;
    text-align: center;
    border: none;
    border: 1px solid #ccc;
    vertical-align: middle;
  }
  .d-td:not(.no-p){
    padding: 4px;
  }
  .div-as-button {
    cursor: pointer;
  }
  #page-container {
    margin: 10px 15%;
  }
</style>
