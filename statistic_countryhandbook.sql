--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: statistic_countryhandbook; Type: TABLE; Schema: public; Owner: oleg
--

CREATE TABLE public.statistic_countryhandbook (
    id integer NOT NULL,
    country character varying(255) NOT NULL,
    description character varying(255)
);


ALTER TABLE public.statistic_countryhandbook OWNER TO oleg;

--
-- Name: statistic_countryhandbook_id_seq; Type: SEQUENCE; Schema: public; Owner: oleg
--

CREATE SEQUENCE public.statistic_countryhandbook_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistic_countryhandbook_id_seq OWNER TO oleg;

--
-- Name: statistic_countryhandbook_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: oleg
--

ALTER SEQUENCE public.statistic_countryhandbook_id_seq OWNED BY public.statistic_countryhandbook.id;


--
-- Name: statistic_countryhandbook id; Type: DEFAULT; Schema: public; Owner: oleg
--

ALTER TABLE ONLY public.statistic_countryhandbook ALTER COLUMN id SET DEFAULT nextval('public.statistic_countryhandbook_id_seq'::regclass);


--
-- Data for Name: statistic_countryhandbook; Type: TABLE DATA; Schema: public; Owner: oleg
--

COPY public.statistic_countryhandbook (id, country, description) FROM stdin;
1	AB	АБХАЗИЯ
2	AD	АНДОРРА
3	AE	ОБЪЕДИНЕННЫЕ АРАБСКИЕ ЭМИРАТЫ
4	AF	АФГАНИСТАН
5	AG	АНТИГУА И БАРБУДА
6	AI	АНГИЛЬЯ
7	AL	АЛБАНИЯ
8	AM	АРМЕНИЯ
9	AO	АНГОЛА
10	AQ	АНТАРКТИДА
11	AR	АРГЕНТИНА
12	AS	АМЕРИКАНСКОЕ САМОА
13	AT	АВСТРИЯ
14	AU	АВСТРАЛИЯ
15	AW	АРУБА
16	AX	ЭЛАНДСКИЕ ОСТРОВА
17	AZ	АЗЕРБАЙДЖАН
18	BA	БОСНИЯ И ГЕРЦЕГОВИНА
19	BB	БАРБАДОС
20	BD	БАНГЛАДЕШ
21	BE	БЕЛЬГИЯ
22	BF	БУРКИНА-ФАСО
23	BG	БОЛГАРИЯ
24	BH	БАХРЕЙН
25	BI	БУРУНДИ
26	BJ	БЕНИН
27	BL	СЕН-БАРТЕЛЕМИ
28	BM	БЕРМУДЫ
29	BN	БРУНЕЙ-ДАРУССАЛАМ
30	BO	БОЛИВИЯ, МНОГОНАЦИОНАЛ. ГОСУДАРСТВО
31	BQ	БОНЭЙР,СИНТ-ЭСТАТИУС И САБА
32	BR	БРАЗИЛИЯ
33	BS	БАГАМЫ
34	BT	БУТАН
35	BV	ОСТРОВ БУВЕ
36	BW	БОТСВАНА
37	BY	БЕЛАРУСЬ
38	BZ	БЕЛИЗ
39	CA	КАНАДА
40	CC	КОКОСОВЫЕ (КИЛИНГ) ОСТРОВА
41	CD	КОНГО, ДЕМОКРАТИЧЕСКАЯ РЕСПУБЛИКА
42	CF	ЦЕНТРАЛЬНО-АФРИКАНСКАЯ РЕСПУБЛИКА
43	CG	КОНГО
44	CH	ШВЕЙЦАРИЯ
45	CI	КОТ Д'ИВУАР
46	CK	ОСТРОВА КУКА
47	CL	ЧИЛИ
48	CM	КАМЕРУН
49	CN	КИТАЙ
50	CO	КОЛУМБИЯ
51	CR	КОСТА-РИКА
52	CU	КУБА
53	CV	КАБО-ВЕРДЕ
54	CW	КЮРАСАО
55	CX	ОСТРОВ РОЖДЕСТВА
56	CY	КИПР
57	CZ	ЧЕХИЯ
58	DE	ГЕРМАНИЯ
59	DJ	ДЖИБУТИ
60	DK	ДАНИЯ
61	DM	ДОМИНИКА
62	DO	ДОМИНИКАНСКАЯ РЕСПУБЛИКА
63	DZ	АЛЖИР
64	EC	ЭКВАДОР
65	EE	ЭСТОНИЯ
66	EG	ЕГИПЕТ
67	EH	ЗАПАДНАЯ САХАРА
68	ER	ЭРИТРЕЯ
69	ES	ИСПАНИЯ
70	ET	ЭФИОПИЯ
71	EU	СТРАНЫ ЕС
72	FI	ФИНЛЯНДИЯ
73	FJ	ФИДЖИ
74	FK	ФОЛКЛЕНДСКИЕ ОСТРОВА (МАЛЬВИНСКИЕ)
75	FM	МИКРОНЕЗИЯ, ФЕДЕРАТИВНЫЕ ШТАТЫ
76	FO	ФАРЕРСКИЕ ОСТРОВА
77	FR	ФРАНЦИЯ
78	GA	ГАБОН
79	GB	СОЕДИНЕННОЕ КОРОЛЕВСТВО
80	GD	ГРЕНАДА
81	GE	ГРУЗИЯ
82	GF	ФРАНЦУЗСКАЯ ГВИАНА
83	GG	ГЕРНСИ
84	GH	ГАНА
85	GI	ГИБРАЛТАР
86	GL	ГРЕНЛАНДИЯ
87	GM	ГАМБИЯ
88	GN	ГВИНЕЯ
89	GP	ГВАДЕЛУПА
90	GQ	ЭКВАТОРИАЛЬНАЯ ГВИНЕЯ
91	GR	ГРЕЦИЯ
92	GS	ЮЖН.ДЖОРДЖИЯ И ЮЖН.САНДВИЧ.ОСТРОВА
93	GT	ГВАТЕМАЛА
94	GU	ГУАМ
95	GW	ГВИНЕЯ-БИСАУ
96	GY	ГАЙАНА
97	HK	ГОНКОНГ
98	HM	ОСТРОВ ХЕРД И ОСТРОВА МАКДОНАЛЬД
99	HN	ГОНДУРАС
100	HR	ХОРВАТИЯ
101	HT	ГАИТИ
102	HU	ВЕНГРИЯ
103	ID	ИНДОНЕЗИЯ
104	IE	ИРЛАНДИЯ
105	IL	ИЗРАИЛЬ
106	IM	ОСТРОВ МЭН
107	IN	ИНДИЯ
108	IO	БРИТАНСКАЯ ТЕРРИТОРИЯ В ИНД.ОКЕАНЕ
109	IQ	ИРАК
110	IR	ИРАН, ИСЛАМСКАЯ РЕСПУБЛИКА
111	IS	ИСЛАНДИЯ
112	IT	ИТАЛИЯ
113	JE	ДЖЕРСИ
114	JM	ЯМАЙКА
115	JO	ИОРДАНИЯ
116	JP	ЯПОНИЯ
117	KE	КЕНИЯ
118	KG	КИРГИЗИЯ
119	KH	КАМБОДЖА
120	KI	КИРИБАТИ
121	KM	КОМОРЫ
122	KN	СЕНТ-КИТС И НЕВИС
123	KP	КОРЕЯ, НАРОДНО-ДЕМОКРАТИЧ.РЕСПУБЛ.
124	KR	КОРЕЯ, РЕСПУБЛИКА
125	KW	КУВЕЙТ
126	KY	ОСТРОВА КАЙМАН
127	KZ	КАЗАХСТАН
128	LA	ЛАОССКАЯ НАРОДНО-ДЕМОК. РЕСПУБЛИКА
129	LB	ЛИВАН
130	LC	СЕНТ-ЛЮСИЯ
131	LI	ЛИХТЕНШТЕЙН
132	LK	ШРИ-ЛАНКА
133	LR	ЛИБЕРИЯ
134	LS	ЛЕСОТО
135	LT	ЛИТВА
136	LU	ЛЮКСЕМБУРГ
137	LV	ЛАТВИЯ
138	LY	ЛИВИЯ
139	MA	МАРОККО
140	MC	МОНАКО
141	MD	МОЛДОВА, РЕСПУБЛИКА
142	ME	ЧЕРНОГОРИЯ
143	MF	СЕН-МАРТЕН
144	MG	МАДАГАСКАР
145	MH	МАРШАЛЛОВЫ ОСТРОВА
146	MK	РЕСПУБЛИКА МАКЕДОНИЯ
147	ML	МАЛИ
148	MM	МЬЯНМА
149	MN	МОНГОЛИЯ
150	MO	МАКАО
151	MP	СЕВЕРНЫЕ МАРИАНСКИЕ ОСТРОВА
152	MQ	МАРТИНИКА
153	MR	МАВРИТАНИЯ
154	MS	МОНТСЕРРАТ
155	MT	МАЛЬТА
156	MU	МАВРИКИЙ
157	MV	МАЛЬДИВЫ
158	MW	МАЛАВИ
159	MX	МЕКСИКА
160	MY	МАЛАЙЗИЯ
161	MZ	МОЗАМБИК
162	NA	НАМИБИЯ
163	NC	НОВАЯ КАЛЕДОНИЯ
164	NE	НИГЕР
165	NF	ОСТРОВ НОРФОЛК
166	NG	НИГЕРИЯ
167	NI	НИКАРАГУА
168	NL	НИДЕРЛАНДЫ
169	NNN	НЕИЗВЕСТНАЯ СТРАНА
170	NO	НОРВЕГИЯ
171	NP	НЕПАЛ
172	NR	НАУРУ
173	NU	НИУЭ
174	NZ	НОВАЯ ЗЕЛАНДИЯ
175	OM	ОМАН
176	OS	ЮЖНАЯ ОСЕТИЯ
177	PA	ПАНАМА
178	PE	ПЕРУ
179	PF	ФРАНЦУЗСКАЯ ПОЛИНЕЗИЯ
180	PG	ПАПУА НОВАЯ ГВИНЕЯ
181	PH	ФИЛИППИНЫ
182	PK	ПАКИСТАН
183	PL	ПОЛЬША
184	PM	СЕНТ-ПЬЕР И МИКЕЛОН
185	PN	ПИТКЕРН
186	PR	ПУЭРТО-РИКО
187	PS	ПАЛЕСТИНА,ГОСУДАРСТВО
188	PT	ПОРТУГАЛИЯ
189	PW	ПАЛАУ
190	PY	ПАРАГВАЙ
191	QA	КАТАР
192	RE	РЕЮНЬОН
193	RO	РУМЫНИЯ
194	RS	СЕРБИЯ
195	RU	РОССИЯ
196	RW	РУАНДА
197	SA	САУДОВСКАЯ АРАВИЯ
198	SB	СОЛОМОНОВЫ ОСТРОВА
199	SC	СЕЙШЕЛЫ
200	SD	СУДАН
201	SE	ШВЕЦИЯ
202	SG	СИНГАПУР
203	SH	СВ.ЕЛЕНА,О.ВОЗНЕС.,ТРИСТАН-ДА-КУНЬЯ
204	SI	СЛОВЕНИЯ
205	SJ	ШПИЦБЕРГЕН И ЯН МАЙЕН
206	SK	СЛОВАКИЯ
207	SL	СЬЕРРА-ЛЕОНЕ
208	SM	САН-МАРИНО
209	SN	СЕНЕГАЛ
210	SO	СОМАЛИ
211	SR	СУРИНАМ
212	SS	ЮЖНЫЙ СУДАН
213	ST	САН-ТОМЕ И ПРИНСИПИ
214	SV	ЭЛЬ-САЛЬВАДОР
215	SX	СЕН-МАРТЕН(НИДЕРЛАНДСКАЯ ЧАСТЬ)
216	SY	СИРИЙСКАЯ АРАБСКАЯ РЕСПУБЛИКА
217	SZ	СВАЗИЛЕНД
218	TC	ОСТРОВА ТЕРКС И КАЙКОС
219	TD	ЧАД
220	TF	ФРАНЦУЗСКИЕ ЮЖНЫЕ ТЕРРИТОРИИ
221	TG	ТОГО
222	TH	ТАИЛАНД
223	TJ	ТАДЖИКИСТАН
224	TK	ТОКЕЛАУ
225	TL	ТИМОР-ЛЕСТЕ
226	TM	ТУРКМЕНИЯ
227	TN	ТУНИС
228	TO	ТОНГА
229	TR	ТУРЦИЯ
230	TT	ТРИНИДАД И ТОБАГО
231	TV	ТУВАЛУ
232	TW	ТАЙВАНЬ (КИТАЙ)
233	TZ	ТАНЗАНИЯ, ОБЪЕДИНЕННАЯ РЕСПУБЛИКА
234	UA	УКРАИНА
235	UG	УГАНДА
236	UM	МАЛЫЕ ТИХООКЕАН.ОТДАЛЕН.ОСТ-ВА С.Ш.
237	US	СОЕДИНЕННЫЕ ШТАТЫ
238	UY	УРУГВАЙ
239	UZ	УЗБЕКИСТАН
240	VA	ПАПСКИЙ ПРЕСТОЛ(ГОС.-ГОРОД ВАТИКАН)
241	VC	СЕНТ-ВИНСЕНТ И ГРЕНАДИНЫ
242	VE	ВЕНЕСУЭЛА,БОЛИВАРИАНСКАЯ РЕСПУБЛИКА
243	VG	ВИРГИНСКИЕ ОСТРОВА, БРИТАНСКИЕ
244	VI	ВИРГИНСКИЕ ОСТРОВА, США
245	VN	ВЬЕТНАМ
246	VU	ВАНУАТУ
247	WF	УОЛЛИС И ФУТУНА
248	WS	САМОА
249	YE	ЙЕМЕН
250	YT	МАЙОТТА
251	YY	ГРУЗИЯ (вне СНГ)
252	ZA	ЮЖНАЯ АФРИКА
253	ZM	ЗАМБИЯ
254	ZW	ЗИМБАБВЕ
\.


--
-- Name: statistic_countryhandbook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: oleg
--

SELECT pg_catalog.setval('public.statistic_countryhandbook_id_seq', 254, true);


--
-- Name: statistic_countryhandbook statistic_countryhandbook_pkey; Type: CONSTRAINT; Schema: public; Owner: oleg
--

ALTER TABLE ONLY public.statistic_countryhandbook
    ADD CONSTRAINT statistic_countryhandbook_pkey PRIMARY KEY (id);


--
-- Name: statistic_countryhandbook_country_2b215c41; Type: INDEX; Schema: public; Owner: oleg
--

CREATE INDEX statistic_countryhandbook_country_2b215c41 ON public.statistic_countryhandbook USING btree (country);


--
-- Name: statistic_countryhandbook_country_2b215c41_like; Type: INDEX; Schema: public; Owner: oleg
--

CREATE INDEX statistic_countryhandbook_country_2b215c41_like ON public.statistic_countryhandbook USING btree (country varchar_pattern_ops);


--
-- PostgreSQL database dump complete
--

