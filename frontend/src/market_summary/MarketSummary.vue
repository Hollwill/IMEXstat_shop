<template>
    <div id="MarketSummary">
        <h1>Сводка рынка</h1>
        <table>
            <tr><th>Импорт</th></tr>
            <tr>
                <th>Стоимость</th>
                <th>Вес</th>
            </tr>
            <tr>
                <th>{{ imp.cost }}</th>
                <th>{{ imp.weight }}</th>
            </tr>
            <tr>
                <th>Вовлеченных стран</th>
                <th>{{ imp.country }}</th>
                <th>Ключевой продукт</th>
                <th>{{ imp.tnved }}</th>
            </tr>
        </table>
        <table>
             <tr><th>Экспорт</th></tr>
            <tr>
                <th>Стоимость</th>
                <th>Вес</th>
            </tr>
            <tr>
                <th>{{ exp.cost }}</th>
                <th>{{ exp.weight }}</th>
            </tr>
            <tr>
                <th>Вовлеченных стран</th>
                <th>{{ exp.country }}</th>
                <th>Ключевой продукт</th>
                <th>{{ exp.tnved }}</th>
            </tr>
        </table>
    </div>
</template>

<script>
    import {HTTP} from '../http-common'
    import moment from 'moment'


    export default {
        name: "MarketSummary",
        props: ['date'],
        data() {
            return {
                imp: {
                    cost: '',
                    weight: '',
                    country: '',
                    tnved: '',
                },
                exp: {
                    cost: '',
                    weight: '',
                    country: '',
                    tnved: '',
                },
            }
        },
        methods: {
            recount() {
                HTTP.get('statistic/market_summary/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from  : moment(new Date()).subtract(1, 'year').format('YYYY-MM')
                    }
                })
                    .then(response => {
                        this.imp = response.data.imp;
                        this.exp = response.data.exp;
                    })
                    .catch(error => {
                        window.console.log(error)
                    })
            }
        },
        created() {
            this.$eventHub.$on('recount', this.recount)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
        mounted() {
            this.recount()

        },
    }
</script>

<style scoped>
table {border: 1px solid grey;}

th {border: 1px solid grey;}

td {border: 1px solid grey;}

table {width: 100%;}

table {width: 600px;}
</style>