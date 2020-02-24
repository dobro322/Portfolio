<template>
  <v-container>
    <v-form ref="form">
      <v-layout column align-center justify-center wrap>
        <v-flex>
          <v-card max-width="500px">
            <v-card-title class="text-xs-center headline font-weight-medium">Опрос студентов СПбГУТ по качеству образования</v-card-title>
            <v-card-text>
              <v-layout v-if="!selected_group" wrap>
                <v-flex text-xs-center md6 offset-md3 xs10 offset-xs1>
                  <v-autocomplete color="orange" label="Номер группы" v-model="current_group" :items="groups.map(a=>{return a.name})" persistent-hint  prepend-icon="supervisor_account"></v-autocomplete>
                  Введи и сработает поиск
                </v-flex>
                <v-flex>
                  <v-layout text-xs-center>
                    <v-flex>
                      <v-btn @click="get_group" class="orange white--text" :disabled="!current_group">Подтвердить</v-btn>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-else text-xs-center>
                <v-flex>
                  <div class="orange--text display-2 font-weight-black">
                    {{ selected_group.name }}
                  </div>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex v-if="selected_group" py-4>
          <v-card max-width="500px">
            <v-card-title class="text-xs-center headline font-weight-medium">Общие вопросы</v-card-title>
            <v-card-text>
              <v-layout wrap column>
                <v-flex pa-2 xs12 v-for="qs in common_questions">
                  <div class="title font-weight-light">{{ qs.question }}</div>
                  <div class="pa-2 text-xs-center" v-if="qs.type == 'rating'">
                    <v-rating medium v-model="qs.answer" color="orange"></v-rating>
                    <div v-if="qs.answer < 5 && qs.additional && qs.answer != 0" class="title font-weight-light">{{ qs.additional.question }}</div>
                    <div v-if="qs.answer < 5 && qs.additional && qs.answer != 0">
                      <v-textarea :rules="[rules.required]" v-if="qs.additional.type == 'comment'" v-model="qs.additional.answer" color = "orange" label="Комментарий"></v-textarea>
                      <v-switch v-if="qs.additional.type == 'yn'" v-model="qs.additional.answer" color="orange" :label="qs.additional.answer ? 'Да' : 'Нет'"></v-switch>
                      <v-rating :rules="[rules.required]" v-if="qs.additional.type == 'rating'" medium v-model="qs.additional.answer" color="orange"></v-rating>
                    </div>
                  </div>
                  <div v-if="qs.type == 'yn'">
                    <v-switch v-model="qs.answer" color="orange" :label="qs.answer ? 'Да' : 'Нет'"></v-switch>
                    <div v-if="!qs.answer && qs.additional" class="pa-2 text-xs-center title font-weight-light">{{ qs.additional.question }}</div>
                    <div v-if="!qs.answer && qs.additional">
                      <v-textarea :rules="[rules.required]" v-if="qs.additional.type == 'comment'" v-model="qs.additional.answer" color = "orange" label="Комментарий"></v-textarea>
                      <v-switch v-if="qs.additional.type == 'yn'" v-model="qs.additional.answer" color="orange" :label="qs.additional.answer ? 'Да' : 'Нет'"></v-switch>
                      <v-rating :rules="[rules.required]" v-if="qs.additional.type == 'rating'" medium v-model="qs.additional.answer" color="orange"></v-rating>
                    </div>
                  </div>
                  <div v-if="qs.type == 'comment'">
                    <v-textarea :rules="[rules.required]" v-model="qs.answer" color = "orange" label="Комментарий"></v-textarea>
                  </div>
                  <v-divider></v-divider>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <div class="pb-3 text-xs-center display-1 font-weight-light orange--text" v-if="selected_group">Раздел по предметам</div>
        <v-flex v-if="selected_group">
          <div class="headline text-xs-center">1 семестр 2018/2019</div>
          <v-card class="my-3" v-for="discipline in articles.first" max-width="500px">
            <v-card-title class="text-xs-left headline font-weight-semibold">{{discipline.header}}</v-card-title>
            <v-card-text>
                  <v-layout align-center row wrap>
                    <v-flex xs12 md6>
                      <div class="headline font-weight-light">Оценка предмета:</div>
                    </v-flex>
                    <v-flex xs12 md6>
                      <v-rating :rules="[rules.required]" medium v-model="discipline.rating" color="orange"></v-rating>
                    </v-flex>
                    <div class="title font-weight-light">Что стоит добавить или убрать по предмету:</div>
                    <v-flex xs12>
                      <v-textarea :rules="[rules.required]" v-model="discipline.comment" color="orange" label="Комментарий"></v-textarea>
                    </v-flex>
                    <div class="headline font-weight-light">Преподаватели:</div>
                    <v-flex mt-2 xs12 v-for="lect in discipline.lecturers" :key="discipline.name">
                      <v-layout align-center row wrap>
                        <v-flex md6 xs12>
                          <div class="title font-weight-light">
                            {{ lect.name }}
                          </div>
                        </v-flex>
                        <v-flex md6 xs12>
                          <v-rating :rules="[rules.required]" medium v-model="lect.rating" color="orange"></v-rating>
                        </v-flex>
                        <v-flex>
                          <v-textarea :rules="[rules.required]" v-model="lect.comment" color = "orange" hint="Улучшить подачу/изменить подход и др." label="Комментарий по преподавателю"></v-textarea>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex py-4 v-if="selected_group">
          <div class="headline text-xs-center">2 семестр 2018/2019</div>
          <v-card class="my-3" v-for="discipline in articles.second" max-width="500px">
            <v-card-title class="text-xs-left headline font-weight-semibold">{{discipline.header}}</v-card-title>
            <v-card-text>
                  <v-layout align-center row wrap>
                    <v-flex xs12 md6>
                      <div class="headline font-weight-light">Оценка предмета:</div>
                    </v-flex>
                    <v-flex xs12 md6>
                      <v-rating :rules="[rules.required]" medium v-model="discipline.rating" color="orange"></v-rating>
                    </v-flex>
                    <div class="title font-weight-light">Что стоит добавить или убрать по предмету:</div>
                    <v-flex xs12>
                      <v-textarea :rules="[rules.required]" v-model="discipline.comment" color="orange" label="Комментарий"></v-textarea>
                    </v-flex>
                    <div class="headline font-weight-light">Преподаватели:</div>
                    <v-flex mt-2 xs12 v-for="lect in discipline.lecturers" :key="discipline.name">
                      <v-layout align-center row wrap>
                        <v-flex md6 xs12>
                          <div class="title font-weight-light">
                            {{ lect.name }}
                          </div>
                        </v-flex>
                        <v-flex md6 xs12>
                          <v-rating :rules="[rules.required]" medium v-model="lect.rating" color="orange"></v-rating>
                        </v-flex>
                        <v-flex>
                          <v-textarea :rules="[rules.required]" v-model="lect.comment" color = "orange" hint="Улучшить подачу/изменить подход и др." label="Комментарий по преподавателю"></v-textarea>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex pb-4 v-if="selected_group">
          <v-card max-width="500px">
            <v-card-title class="text-xs-left headline font-weight-semibold">Дисциплины по выбору</v-card-title>
            <v-card-text>
              <v-layout row wrap>
                <v-flex>
                  <div class="headline font-weight-light">Были ли у вас дисциплины по выбору?</div>
                </v-flex>
                <v-flex>
                  <v-switch label="Да" v-model="choise_articles.existing" color="orange"></v-switch>
                </v-flex>
                <v-flex v-if="choise_articles.existing">
                  <div class="headline font-weight-light">Оцените полезность данной системы:</div>
                  <v-rating :rules="[rules.required]" medium color="orange" v-model="choise_articles.rating"></v-rating>
                </v-flex>
                <v-flex v-if="choise_articles.existing">
                  <div class="headline font-weight-light">Давали ли вам право выбора дисциплин?</div>
                  <v-radio-group v-model="choise_articles.choise">
                    <v-radio color="orange" label="Деканат говорил, что выбирать" value="Деканат"></v-radio>
                    <v-radio color="orange" label="Я выбирал сам"value="Сам"></v-radio>
                  </v-radio-group>
                </v-flex>
                <v-flex v-if="choise_articles.existing">
                  <div class="headline font-weight-light">Оставьте пожелания и жалобы по дисциплинам по выбору:</div>
                  <v-textarea :rules="[rules.required]" color="orange" v-model="choise_articles.comment" label="Комментарий"></v-textarea>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex v-if="selected_group">
          <v-card max-width="500px">
            <v-card-title class="text-xs-left headline font-weight-semibold">Персональные данные</v-card-title>
            <v-card-text>
              <div>Главная задача этого опроса - оказать влияние на составление учебных планов следующих лет.<br>
              <br>Вы имеете полное право отказаться от предоставления личной информации, но тогда мы не сможем использовать Ваш отзыв при аргументировании и внесении изменений.<br>
              <br>Если Вы заинтересованны в дальнейшем улучшении качества образования СПбГУТ, то убедительно просим Вас оставить свои данные.<br>
              <br>В случае Вашего отказа, мы все равно будем использовать предоставленную информацию в дальнейшем улучшении качества образования, а также при статистических подсчетах и аналитике</div>
              <v-radio-group v-model="user.future">
                <v-radio color="orange" label="Готов предоставить ПД для улучшения качества образлвания" :value="true"></v-radio>
                <v-radio color="orange" label="Отказываюсь от предоставления ПД" :value="false"></v-radio>
              </v-radio-group>
              <div class="ma-4" v-if="user.future">
                <v-text-field :rules=[rules.required] label="Ваше ФИО" color="orange" v-model="user.name"  persistent-hint  prepend-icon="person"></v-text-field>
                <v-layout align-center row wrap>
                  <v-flex xs12>
                    <div>В соответствии с п.4 ст.9 Федерального закона «О персональных данных» от 27.07.2006 года № 152-ФЗ, даю согласие Комитету по качеству образования Студенческого совета СПбГУТ на обработку моих персональных данных (Ф.И.О., номер группы), т.е. на совершение действий, предусмотренных Федеральным законом «О персональных данных» от 27.07.2006 года № 152-ФЗ.</div>
                  </v-flex>
                  <v-flex xs12>
                    <v-checkbox color="orange" label="Даю согласие" v-model="user.agreement" value="true"></v-checkbox>
                  </v-flex>
                </v-layout>
              </div>
              <v-layout v-if="user.future!=null" row wrap>
                <v-flex text-xs-center>
                  <v-dialog max-width="500px">
                    <v-btn large color="orange" dark slot="activator">Отправить</v-btn>
                    <v-card>
                      <v-card-title class="headline">Привет, это твой убер-опрос!</v-card-title>
                      <v-card-text>
                        <v-layout text-xs-center column>
                          <div class="subheading">
                            <p>Подтверждаешь отправку данных?</p>
                            <p>Изменить уже не получится</p>
                          </div>
                          <v-btn dark @click="recaptcha" color="orange">Подтвердить</v-btn>
                        </v-layout>
                      </v-card-text>
                    </v-card>
                  </v-dialog>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-form>
  </v-container>
</template>
<script src="https://www.google.com/recaptcha/api.js?render=6LdIb60UAAAAAAEEbQYN0DxRfW5HR1UYtP-JKYrY"></script>
<script>
import axios from 'axios';

  export default {
    data() {
      return{
        rules: {
         required: value => !!value || 'Обязательное поле.',
        },
        common_questions: [
          {
            question: "На сколько вы оцениваете качество образования СПбГУТ?",
            type: "rating",
            answer: 0,
            additional: {
              question: "Что вас не устраивает и есть ли у вас предложения по улучшению?",
              type: "comment",
              answer: null
            }
          },
          {
            question: "Устраивает ли вас образовательная программа?",
            type: "yn",
            answer: true,
            additional: {
              question: "Что вас не устраивает и есть ли у вас предложения по улучшению?",
              type: "comment",
              answer: null
            }
          },
          {
            question: "Устраивает ли вас последовательность учебной программы?",
            type: "yn",
            answer: true,
            additional: {
              question: "Что вас не устраивает и есть ли у вас предложения по улучшению?",
              type: "comment",
              answer: null
            }
          },
          {
            question: "Есть ли у вас ещё пожелания/просьбы/жалобы по поводу учебной программы СПбГУТ?",
            type: "comment",
            answer: null
          },
        ],
        groups: [],
        articles: {first: [], second: []},
        current_group: null,
        selected_group: null,
        user: {
          name: "",
          agreement: false,
          future: null
        },
        choise_articles: {
          existing: false,
          rating: 0,
          choise: "",
          comment: null
        }
      }
    },
    created(){
       axios.post("https://educationsut.ru/api/groups").then((resp) => {
         this.groups = resp.data
       })
    },
    methods:{
      recaptcha() {
        this.$refs.form.validate()
        this.$recaptcha('homepage').then((token) => {
          const data = {
            "token": token,
            "group": this.current_group,
            "common": this.common_questions,
            "first": this.articles.first,
            "second": this.articles.second,
            "choice": this.choise_articles,
            "user": this.user
          }
          axios.post("https://educationsut.ru/api/new_answer", data).then((resp) => {
            localStorage.token = resp.data.token
          })
        })
      },
      get_group(){
        const data = {
          name: this.current_group
        }
        axios.post("https://educationsut.ru/api/get", data).then((resp) => {
          this.selected_group = resp.data
          for (var discipline of resp.data.articles.first) {
            var lects = []
            for (var lect in discipline.lecturers) {
              var t = this.convert_lecturers(discipline.lecturers[lect])
              t != null ? lects = lects.concat(t) : 1
            }
            lects = this.distinct_lecturers(lects)
            var data = {
              header: discipline.header,
              rating: 0,
              comment: null,
              lecturers: lects.map(a => {return {name: a, rating: 0, comment: null}})
            }
            this.articles.first.push(data)
          }
          for (discipline of resp.data.articles.second) {
            var lects = []
            for (var lect in discipline.lecturers) {
              var t = this.convert_lecturers(discipline.lecturers[lect])
              t != null ? lects = lects.concat(t) : 1
            }
            lects = this.distinct_lecturers(lects)
            var data = {
              header: discipline.header,
              rating: 0,
              comment: null,
              lecturers: lects.map(a => {return {name: a, rating: 0, comment: null}})
            }
            this.articles.second.push(data)
          }
        })
      },
      convert_lecturers(arr){
        if (arr){
          var str = arr.split('/')
          var tmp = []
          for (var variable of str) {
            tmp.push(variable.trim())
          }
          return tmp
        }
      },
      distinct_lecturers(arr){
        function onlyUnique(value, index, self) {
            return self.indexOf(value) === index;
        }
        return arr.filter( onlyUnique )
      }
    }
  }
</script>

<style>

</style>
