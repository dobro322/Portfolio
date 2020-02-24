<template>
  <v-content>



    <v-layout class="px-4 pt-4" column wrap>
      <p>Дата</p>
      <v-layout row wrap>
        <v-flex xs12 sm2>
          <v-select
            :items="generate_dates.map(a=>{return a.readable_formant})"
            v-model="date"
            @input="select_day"
            color="purple"
            style="font-size:25px"
          ></v-select>
        </v-flex>
      </v-layout>
      <p>Время</p>
      <v-layout align-center justify-start row wrap>
        <div>
          <v-select
            :items="['10','11','12','13','14','15','16','17','18','19']"
            v-model="time.hours"
            color="purple"
            style="font-size:42px; width:50px"
          ></v-select>
        </div>
        <div class="display-2"><p>:</p></div>
        <div>
          <v-select
            :items="['00','15','30','45']"
            v-model="time.minutes"
            color="purple"
            style="font-size:42px; width:50px"
          ></v-select>
        </div>
      </v-layout>
    </v-layout>

    <v-layout row wrap>
      <v-flex lg2 md3 sm4 xs12 class="pa-2" v-for="(place, index) in places" :key="index">
        <PlaceCard
          ref="PlaceCard"
          :place="place"
          :chosen_date="chosen_date"
          :chosen_time="sum_time"
          @change_time="change_time"
        >
        </PlaceCard>
      </v-flex>
    </v-layout>

  </v-content>
</template>
<script>
import axios from 'axios'
import format from 'date-fns/format'
import PlaceCard from '../components/PlaceCard.vue'
import ru from 'date-fns/locale/ru'

  export default {
    components:{PlaceCard},
    computed:{
      sum_time:{
        get(){
          return this.time.hours + ":" + this.time.minutes
        },
        set(arg){
          this.time.hours = arg[0] + arg[1]
          this.time.minutes = arg[3] + arg[4]
        }
      },
      generate_dates(){
        Date.prototype.addDays = function(days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
      }

      function getDates(startDate, stopDate) {
          var dateArray = new Array();
          var currentDate = startDate;
          while (currentDate <= stopDate) {
              dateArray.push(
                {
                  "readable_formant": format(new Date (currentDate), 'D.MM - dddd', {locale: ru}),
                  "date_format": new Date (currentDate)
                }
              );
              currentDate = currentDate.addDays(1);
          }
          return dateArray;
      }
      var date = new Date()
      var range = getDates(new Date(date.getFullYear(),date.getMonth(), date.getDate(),0,0,0,0), new Date(date.getFullYear(),date.getMonth(), date.getDate(),0,0,0,0).addDays(14));
      return range

      },
      generate_time(){
        var dateArray = new Array();
        var h = "10"
        var m = "00"
        for(var i = 0; i < 10; i++){
          m = "00"
          for(var j = 0; j < 4; j++){
            dateArray.push(h + ":" + m)
            m = parseInt(m) + 15
          }
          h = parseInt(h) + 1
        }

        return dateArray

      }
    },
    methods: {
      change_time(arg){
        this.sum_time = arg
      },
      formattedDate(arg){
        return arg ? format(new Date(arg*1000), 'H:mm D.MM') : ''
      },
      select_day(arg){
        var t = this.generate_dates.find(a=>{return a.readable_formant === this.date ? 1 : 0}).date_format
        var asd = Date.parse(t)/1000
        this.chosen_date = asd
      },
    },
    data(){
      return{
        date: "",
        chosen_date: "",
        time: {
          sum: this.sum_time,
          hours: "10",
          minutes: "00"
        },
        places: [
          {
            "id": 1,
            "name": "Холл Грифона",
            "description": "1 корпус  2 этаж (дальний от метро)",
            "photo": "https://sun9-56.userapi.com/c850224/v850224747/1d0fec/2e4NP37BzuY.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              },
              {
                "time_start": 1568829600,
                "time_end": 1568836800,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 2,
            "name": "Холл Лисы",
            "description": "1 корпус 3 этаж (ближе к метро)",
            "photo": "https://sun9-54.userapi.com/c858028/v858028763/7a287/NgD_f6rSUv8.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 3,
            "name": "Холл Дракона",
            "description": "1 корпус 4 этаж (ближе к метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 4,
            "name": "Холл Моржа",
            "description": "1 корпус 4 этаж (дальше от метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 5,
            "name": "Холл Собаки",
            "description": "Х1 корпус 6 этаж (дальний от метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 6,
            "name": "Холл Оленя",
            "description": "1 корпус 6 этаж (ближний к метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 7,
            "name": "Холл Медведя",
            "description": "1 корпус 7 этаж (ближний к метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 8,
            "name": "Холл Филина",
            "description": "1 корпус 7 этаж (дальний от метро)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          },
          {
            "id": 9,
            "name": "Холл Калибри",
            "description": "2 корпус 4 этаж (комната отдыха)",
            "photo": "https://sun9-37.userapi.com/c854216/v854216528/f721b/T1gebSBZOMo.jpg",
            "reservation_time": [
              {
                "time_start": 1568800800,
                "time_end": 1568811600,
                "reserved_by": {
                  "name": "Ковальчук Владислав",
                  "id": "vladhasnoid"
                }
              }
            ],
          }
        ]
      }
    },
    created(){

    }
}
</script>

<style>
.v-text-field .v-input__append-inner {
    display: none;
}
</style>
