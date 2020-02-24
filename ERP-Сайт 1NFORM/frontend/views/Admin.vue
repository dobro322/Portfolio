<template>
  <v-container fluid>
    <v-layout v-if="check_role() === '794'" justify-space-around row wrap>

      <v-flex pb-4 xs12 md5>
        <v-card>
          <v-layout column align-center wrap>
            <v-flex class="headline"><p>Новый слот</p></v-flex>
            <v-flex>
              <v-btn flat color="orange" prepend-icon>
                <input class='file-input' type="file" @change="onShopFileChange" />
                <v-icon left>cloud_upload</v-icon>
                <p>Загрузить файл</p>
              </v-btn>
            </v-flex>
            <v-form ref="shop_form">
              <v-flex v-if="shop_url">
                <v-layout px-4 row wrap>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Заголовок"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Описание"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Стоимость"
                    ></v-text-field>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-form>
          </v-layout>
          <v-card-actions>
            <v-layout v-if="shop_url" justify-center row wrap>
              <v-btn flat color="orange" @click="add_shop" large><p>Добавить</p></v-btn>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex pb-4 xs12 md5>
        <v-card>
          <v-layout column align-center wrap>
            <v-flex class="headline"><p>Новый квест</p></v-flex>
            <v-flex>
              <v-text-field
                label="URL на квест"
                v-model="quest_data.pic.url"
              ></v-text-field>
            </v-flex>
            <v-form ref="quest_form">
              <v-flex v-if="quest_data.pic.url">
                <v-layout px-4 row wrap>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Заголовок"
                      v-model="quest_data.title"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Описание"
                      v-model="quest_data.comment"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      label="Стоимость"
                      v-model="quest_data.cost"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-switch label="Ежедневный" v-model="quest_data.daily"></v-switch>
                  </v-flex>
                  <v-flex xs12>
                    <v-menu
                      :close-on-content-click="false"
                      v-model="date_menu"
                      transition="scale-transition"
                      offset-y
                      :nudge-right="40"
                      max-width="290px"
                      min-width="290px"
                      color="orange"
                    >
                      <v-text-field
                        slot="activator"
                        label="Дедлайн"
                        v-model="quest_data.date_exp"
                        prepend-icon="event"
                        readonly
                        color="orange"
                      ></v-text-field>
                      <v-date-picker color="orange" v-model="quest_data.date_exp" no-title>
                          <v-btn flat color="orange" @click="date_menu = false"><p>Сохранить</p></v-btn>
                      </v-date-picker>
                    </v-menu>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      label="Количество"
                      v-model="quest_data.counting.count"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-autocomplete
                      v-model="quest_data.counting.function"
                      :items="quests.map(a=>{return a.description})"
                      prepend-icon="how_to_reg"
                      label="Как считать будем?"
                    ></v-autocomplete>
                  </v-flex>
                  <v-flex v-if="quest_data.counting.function != 'Никак'" xs12>
                    <v-autocomplete
                      v-model="quest_data.counting.additional.faculty"
                      :items="faculties"
                      prepend-icon="how_to_reg"
                      label="Факульет"
                      multiple
                    ></v-autocomplete>
                  </v-flex>
                  <v-flex xs12>
                    <v-autocomplete
                      v-model="quest_data.audience.faculties"
                      :items="faculties"
                      prepend-icon="how_to_reg"
                      label="Факультеты"
                      multiple
                    ></v-autocomplete>
                  </v-flex>
                  <v-flex xs12>
                    <v-autocomplete
                      v-model="quest_data.audience.departments"
                      :items="departments"
                      prepend-icon="how_to_reg"
                      label="Отделы"
                      multiple
                    ></v-autocomplete>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-form>
          </v-layout>
          <v-card-actions>
            <v-layout v-if="quest_data.pic.url" justify-center row wrap>
              <v-btn flat color="orange" @click="add_quest" large><p>Добавить</p></v-btn>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex pb-4 xs12 md5>

      </v-flex>
      <v-flex align-center text-xs-center pb-4 xs12 md5>
      <div  v-if="quest_data.pic.url">
        <p>Вертикальное</p>
        <v-slider v-model="quest_data.pic.top" :max="500" ></v-slider>
        <p>Горизотальное</p>
        <v-slider v-model="quest_data.pic.left" :max="500" ></v-slider>
        <p>Размер</p>
        <v-slider v-model="quest_data.pic.width" :max="1000" ></v-slider>
      </div>
      <v-layout justify-center row wrap>
        <v-card width="400px" style="display: flex; flex-direction: column;" class="ma-4">
          <v-card height="10px" flat class="pa-1" color="orange"></v-card>
          <div
          :style="'background-size: '+quest_data.pic.width+'px;background-position: '+(-quest_data.pic.left)+'px '+ (-quest_data.pic.top)+'px; background-image:url(' +quest_data.pic.url + ')'"
          class="hidden-sm-and-down"
          >
            <div style="height:250px;background-color:rgb(0,0,0,0.5)" >
              <v-layout v-if="quest_data.counting.count > 1" fill-height align-center row wrap>
                <v-flex class="text-xs-center white--text display-3 font-weight-bold">
                  <p>0/{{ quest_data.counting.count }}</p>
                </v-flex>
              </v-layout>
            </div>
          </div>
          <v-card-title class="grow display-1 justify-center">
            <p>{{quest_data.title}}</p>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout column wrap>
              <v-flex xs12 class="title font-weight-regular">
                <p>{{ quest_data.comment }}</p>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions>
            <v-layout align-center row wrap>
              <v-flex md6 xs12 class="title font-weight-regular">
                <p><v-icon color="red">date_range</v-icon>{{ quest_data.date_exp? formattedDate(quest_data.date_exp):'' }}</p>
              </v-flex>
              <v-flex md6 xs12>
                <v-btn large class="display-1 purple--text text--lighten-1 font-weight-bold" flat><v-icon left>monetization_on</v-icon><p style="line-height:1px" class="museo700">{{ quest_data.cost }}</p></v-btn>
              </v-flex>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-layout>
      </v-flex>
      <v-flex md6 lg4 xs12>
        <v-layout column wrap>
          <v-autocomplete
            v-model="chosen_member"
            :items="members"
            chips
            color="orange"
            label="Ответственные"
            item-text="name"
            return-object
            prepend-icon="people"
          >
            <template
              slot="selection"
              slot-scope="data"
            >
              <v-chip
                :selected="data.selected"
                close
                class="chip--select-multi"
                @input="data.parent.selectItem(data.item)"
              >
                <v-avatar>
                  <img :src="data.item.info.pic">
                </v-avatar>
                {{ data.item.info.name.split(' ')[1] }}
              </v-chip>
            </template>
            <template
              slot="item"
              slot-scope="data"
            >
              <template>
                <v-list-tile-avatar>
                  <img :src="data.item.info.pic">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title v-html="data.item.info.name.split(' ')[1]"></v-list-tile-title>
                  <v-list-tile-sub-title v-html="data.item.info.faculty"></v-list-tile-sub-title>
                </v-list-tile-content>
              </template>
            </template>
          </v-autocomplete>
          <v-autocomplete
            v-model="chosen_quest"
            :items="sorted_quest"
            chips
            color="orange"
            label="Ответственные"
            item-text="name"
            return-object
            prepend-icon="people"
          >
            <template
              slot="selection"
              slot-scope="data"
            >
              <v-chip
                :selected="data.selected"
                close
                class="chip--select-multi"
                @input="data.parent.selectItem(data.item)"
              >
                <v-avatar>
                  <img :src="data.item.pic.url">
                </v-avatar>
                {{ data.item.title }}
              </v-chip>
            </template>
            <template
              slot="item"
              slot-scope="data"
            >
              <template>
                <v-list-tile-avatar>
                  <img :src="data.item.pic.url">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title v-html="data.item.title"></v-list-tile-title>
                  <v-list-tile-sub-title v-html="data.item.text"></v-list-tile-sub-title>
                </v-list-tile-content>
              </template>
            </template>
          </v-autocomplete>
          <v-btn @click="achieve_quest" block ><p>Засчитать</p></v-btn>
        </v-layout>
      </v-flex>
    </v-layout>
    <v-layout class="display-4" v-else text-xs-center justify-center row wrap>
      <p class="museo900">Сорри, нет прав</p>
    </v-layout>
  </v-container>
</template>
<script>
import format from 'date-fns/format'
import axios from 'axios'

  export default {
    computed: {
      sorted_quest(){
        var memb = a => {
          return this.chosen_member ? this.chosen_member.quests.find(b=>{return b.id == a.id}) : false
        }
        return this.all_quests.filter(a=>{return a.counting.function === '' && !memb(a)})
      }
    },
    methods: {
        check_role(){
          return localStorage.role
        },
        formattedDate(arg){
          return format(arg, 'D.MM.YYYY')
        },
       onShopFileChange(e) {
         const file = e.target.files[0];
         if(file) this.shop_url = URL.createObjectURL(file);
       },
       add_quest(){
         if(this.$refs.quest_form.validate()){

           var t = Object.assign({}, this.quest_data)
           t.counting.function = this.quests.find(a=>{return a.description === t.counting.function}).function
           const data = t
           axios.post('https://ocheredsut.ru/api/1/quests/', data).then((resp) => {

           })
         }
       },
       add_shop(){

       },
       achieve_quest(){
         const data = {
           member: this.chosen_member.info.vk,
           quest: this.chosen_quest.id,
         }
         axios.put('https://ocheredsut.ru/api/1/admin/achieve_quest', data).then((resp) => {
         })
       }
     },
    created(){
      axios.get('https://ocheredsut.ru/api/1/admin/').then((resp) => {
        this.quests = resp.data.quests
          this.quests.push({
            "function": "",
            "description": "Никак"
          })
        this.all_quests = resp.data.all_quests
        this.members = resp.data.team
      })
    },
    data(){return{
      chosen_member: null,
      chosen_quest: null,
      all_quests:[],
      members:[],
      quests:[

      ],
      departments: [
        "Собеседники",
        "Серфинг",
        "Фильтрация",
        "SMM",
        "Event",
        "Фандрайзинг",
        "Приемная комиссия"
      ],
      faculties: [
        "ИКСС",
        "ИСиТ",
        "РТС",
        "ГФ",
        "ВУЦ",
        "ЦЭУБИ",
        "ФП",
        "ИНО",
        "СПбКТ"
      ],
      rules: {
        required: value => !!value.replace(/\s+/, "") || 'Обязательное поле',
      },
      date_menu: false,
      members: [],
      quest_data:{
        title: '',
        comment: '',
        pic: {
          url: '',
          top: 0,
          left: 0,
          width: 300
        },
        daily: false,
        date_exp: '',
        audience:{
          faculties: [],
          departments: []
        },
        counting: {
          count: 0,
          function: "",
          additional: {
            faculty: ""
          }
        },
        cost: ''
      },
      shop_data:{
        title: '',
        comment: '',
        cost: 0
      },
      quest_url: '',
      shop_url: '',
    }}
  }
</script>

<style>

#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

.file-btn{
  cursor: pointer;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 10;
  cursor: pointer;
}

#preview img {
  max-height: 400px;
  max-width: 300px;
}
</style>
