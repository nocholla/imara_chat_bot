import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import os
import logging
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval
from src.data_loader import load_config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()
data_dir = config.get('data_dir', 'data')

# FAQ responses from Firestore data
FAQ_RESPONSES = {
    "Initial": {
        "messages": {
            "en": "Hello there! I’m IMARA, your friendly Africa Love Match assistant, here to make things easier for you. What can I help you with today? 😊",
            "ar": "مرحبًا بك! أنا إيمارا، مساعدتك الودودة في Africa Love Match، هنا لتسهيل الأمور عليك. كيف يمكنني مساعدتك اليوم؟ 😊",
            "de": "Hallo! Ich bin IMARA, deine freundliche Assistentin bei Africa Love Match, und ich bin hier, um dir zu helfen. Wobei brauchst du Unterstützung? 😊",
            "es": "¡Hola! Soy IMARA, tu asistente amigable de Africa Love Match, aquí para ayudarte con lo que necesites. ¿En qué puedo ayudarte hoy? 😊",
            "fr": "Coucou ! Je suis IMARA, ton assistante sympa sur Africa Love Match, prête à t’aider. De quoi as-tu besoin aujourd’hui ? 😊",
            "it": "Ciao! Sono IMARA, la tua assistente amichevole di Africa Love Match, qui per semplificarti le cose. Come posso aiutarti oggi? 😊",
            "nl": "Hoi! Ik ben IMARA, jouw vriendelijke assistent bij Africa Love Match, hier om het je makkelijker te maken. Waarmee kan ik je vandaag helpen? 😊",
            "pt": "Olá! Eu sou a IMARA, sua assistente simpática do Africa Love Match, aqui para te ajudar. No que posso te ajudar hoje? 😊"
        },
        "options": [
            {"text": {"en": "Subscription", "ar": "اشتراك", "de": "Abonnement", "es": "Suscripción", "fr": "Abonnement", "it": "Abbonamento", "nl": "Abonnement", "pt": "Assinatura"}, "nextState": "SubscriptionHelp"},
            {"text": {"en": "Account Closed", "ar": "الحساب مغلق", "de": "Konto geschlossen", "es": "Cuenta cerrada", "fr": "Compte fermé", "it": "Account chiuso", "nl": "Account gesloten", "pt": "Conta encerrada"}, "nextState": "AccountClosedHelp"},
            {"text": {"en": "Profile Edit", "ar": "تحرير الملف الشخصي", "de": "Profil bearbeiten", "es": "Editar perfil", "fr": "Modifier le profil", "it": "Modifica del profilo", "nl": "Profiel bewerken", "pt": "Editar perfil"}, "nextState": "ProfileEdit"},
            {"text": {"en": "Privacy and Safety", "ar": "الخصوصية والأمان", "de": "Datenschutz und Sicherheit", "es": "Privacidad y seguridad", "fr": "Confidentialité et sécurité", "it": "Privacy e sicurezza", "nl": "Privacy en veiligheid", "pt": "Privacidade e segurança"}, "nextState": "PrivacySafetyHelp"},
            {"text": {"en": "Report and Block", "ar": "الإبلاغ والحظر", "de": "Melden und blockieren", "es": "Reportar y bloquear", "fr": "Signaler et bloquer", "it": "Segnala e blocca", "nl": "Rapporteer en blokkeer", "pt": "Denunciar e bloquear"}, "nextState": "ReportBlockHelp"},
            {"text": {"en": "Payment and Refund", "ar": "الدفع والاسترداد", "de": "Zahlung und Rückerstattung", "es": "Pago y reembolso", "fr": "Paiement et remboursement", "it": "Pagamento e rimborso", "nl": "Betaling en terugbetaling", "pt": "Pagamento e reembolso"}, "nextState": "PaymentRefundHelp"},
            {"text": {"en": "Matchmaking", "ar": "التوفيق بين الأشخاص", "de": "Partnervermittlung", "es": "Emparejamiento", "fr": "Mise en relation", "it": "Matchmaking", "nl": "Matchmaking", "pt": "Matchmaking"}, "nextState": "MatchmakingHelp"}
        ]
    },
    "SubscriptionHelp": {
        "messages": {
            "en": "Ready to chat with your likes and matches? How exciting! 🎉 Just tap the 'Subscribe' button to get started—it’s so easy! Don’t worry, all payments and cancellations are handled safely through your app store. 😊",
            "ar": "هل أنت مستعد للدردشة مع من أعجبوك وتطابقوا معك؟ يا لها من لحظة مثيرة! 🎉 اضغط على زر 'الاشتراك' لتبدأ—الأمر سهل للغاية! لا داعي للقلق، جميع المدفوعات والإلغاءات تتم بأمان عبر متجر التطبيقات الخاص بك. 😊",
            "de": "Bereit, mit deinen Likes und Matches zu chatten? Wie aufregend! 🎉 Tippe einfach auf den Button 'Abonnieren', um loszugehen – es ist super einfach! Keine Sorge, alle Zahlungen und Kündigungen werden sicher über deinen App Store abgewickelt. 😊",
            "es": "¿Listo para chatear con tus likes y coincidencias? ¡Qué emocionante! 🎉 Solo toca el botón 'Suscribirse' para empezar, ¡es muy fácil! No te preocupes, todos los pagos y cancelaciones se manejan de forma segura a través de tu tienda de aplicaciones. 😊",
            "fr": "Prêt à discuter avec tes likes et matchs ? Trop excitant ! 🎉 Appuie simplement sur le bouton 'S’abonner' pour commencer, c’est vraiment facile ! Pas d’inquiétude, tous les paiements et annulations sont gérés en toute sécurité via ta boutique d’applications. 😊",
            "it": "Pronto a chattare con i tuoi like e match? Che emozione! 🎉 Tocca il pulsante 'Abbonati' per iniziare, è facilissimo! Non preoccuparti, tutti i pagamenti e le cancellazioni sono gestiti in sicurezza tramite il tuo app store. 😊",
            "nl": "Klaar om te chatten met je likes en matches? Wat spannend! 🎉 Tik gewoon op de knop 'Abonneren' om te beginnen, het is zo makkelijk! Maak je geen zorgen, alle betalingen en annuleringen worden veilig afgehandeld via je app store. 😊",
            "pt": "Pronto para conversar com seus likes e matches? Que empolgante! 🎉 Toque no botão 'Assinar' para começar, é muito fácil! Fique tranquilo, todos os pagamentos e cancelamentos são feitos com segurança pela sua loja de aplicativos. 😊"
        },
        "options": [
            {"text": {"en": "Payment & Refunds", "ar": "المدفوعات والاسترداد", "de": "Zahlungen & Rückerstattungen", "es": "Pagos y reembolsos", "fr": "Paiements et remboursements", "it": "Pagamenti e rimborsi", "nl": "Betalingen & terugbetalingen", "pt": "Pagamentos e reembolsos"}, "nextState": "PaymentRefundHelp"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "PaymentRefundHelp": {
        "messages": {
            "en": "Managing your subscription is a breeze! 🎉 You can take care of everything right in your app store account. Just tap 'Subscribe' to join or cancel anytime you want—it’s so simple and hassle-free! 😊",
            "ar": "إدارة اشتراكك أسهل من السهل! 🎉 يمكنك التعامل مع كل شيء مباشرة من حساب متجر التطبيقات الخاص بك. اضغط على 'اشترك' للانضمام أو الإلغاء في أي وقت تريد—بسيط وخالٍ من التعقيد! 😊",
            "de": "Dein Abonnement zu verwalten ist kinderleicht! 🎉 Du kannst alles direkt in deinem App-Store-Konto regeln. Tippe einfach auf 'Abonnieren', um beizutreten oder jederzeit zu kündigen – super einfach und ohne Stress! 😊",
            "es": "¡Gestionar tu suscripción es pan comido! 🎉 Puedes encargarte de todo directamente desde tu cuenta de la tienda de aplicaciones. Solo toca 'Suscribir' para unirte o cancelar cuando desees, ¡es súper sencillo y sin complicaciones! 😊",
            "fr": "Gérer ton abonnement, c’est un jeu d’enfant ! 🎉 Tu peux tout régler directement depuis ton compte App Store. Clique sur 'S’abonner' pour t’inscrire ou annuler à tout moment – c’est hyper simple et sans tracas ! 😊",
            "it": "Gestire il tuo abbonamento è un gioco da ragazzi! 🎉 Puoi occuparti di tutto direttamente dal tuo account sullo store delle app. Tocca 'Iscriviti' per abbonarti o disdire quando vuoi, è facilissimo e senza problemi! 😊",
            "nl": "Je abonnement beheren is een fluitje van een cent! 🎉 Je kunt alles regelen via je app store-account. Tik op 'Abonneren' om je aan te melden of op te zeggen wanneer je maar wilt – zo simpel en zonder gedoe! 😊",
            "pt": "Gerenciar sua assinatura é moleza! 🎉 Você pode cuidar de tudo diretamente pela sua conta na loja de aplicativos. Toque em 'Assinar' para se inscrever ou cancelar a qualquer momento – é muito simples e sem complicações! 😊"
        },
        "options": [
            {"text": {"en": "Account Closed", "ar": "تم إغلاق الحساب", "de": "Konto geschlossen", "es": "Cuenta cerrada", "fr": "Compte fermé", "it": "Account chiuso", "nl": "Account gesloten", "pt": "Conta encerrada"}, "nextState": "AccountClosedHelp"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "AccountClosedHelp": {
        "messages": {
            "en": "Oh no, it seems your account might have been closed due to something like nudity, fake profiles, scams, or copyright issues. If you think this might be a mistake, don’t worry—we’ve got you! 💖 Just reach out to our support team, and they’ll take a closer look for you. We’re here to help! 😊",
            "ar": "يا إلهي، يبدو أن حسابك قد أُغلق بسبب شيء مثل العري، الملفات الشخصية المزيفة، الاحتيال، أو مشكلات حقوق الطبع والنشر. إذا كنت تعتقد أن هذا قد يكون خطأ، لا تقلق—نحن ندعمك! 💖 تواصل مع فريق الدعم لدينا، وسيقومون بمراجعة الأمر عن كثب من أجلك. نحن هنا لمساعدتك! 😊",
            "de": "Oh je, es sieht so aus, als wäre dein Konto vielleicht wegen etwas wie Nacktheit, gefälschten Profilen, Betrug oder Urheberrechtsproblemen geschlossen worden. Falls du denkst, dass das ein Fehler sein könnte, keine Sorge – wir sind bei dir! 💖 Wende dich einfach an unser Support-Team, und sie schauen sich das genauer für dich an. Wir sind für dich da! 😊",
            "es": "¡Vaya, parece que tu cuenta podría haber sido cerrada por algo como desnudez, perfiles falsos, estafas o problemas de derechos de autor! Si crees que esto puede ser un error, no te preocupes, ¡te tenemos cubierto! 💖 Contacta a nuestro equipo de soporte, y ellos lo revisarán más de cerca por ti. ¡Estamos aquí para ayudarte! 😊",
            "fr": "Oh non, il semble que ton compte ait peut-être été fermé à cause de choses comme la nudité, les faux profils, les arnaques ou des problèmes de droits d’auteur. Si tu penses que c’est une erreur, pas de panique, on est là pour toi ! 💖 Contacte notre équipe de support, et ils examineront ça de plus près pour toi. On est là pour t’aider ! 😊",
            "it": "Oh no, sembra che il tuo account possa essere stato chiuso per qualcosa come nudità, profili falsi, truffe o problemi di copyright. Se pensi che potrebbe essere un errore, non preoccuparti: ti copriamo noi! 💖 Contatta il nostro team di supporto, e loro daranno un’occhiata più approfondita per te. Siamo qui per aiutarti! 😊",
            "nl": "O jee, het lijkt erop dat je account mogelijk is gesloten vanwege iets als naaktheid, nepprofielen, oplichting of auteursrechtproblemen. Als je denkt dat dit een vergissing kan zijn, maak je geen zorgen – we staan achter je! 💖 Neem contact op met ons ondersteuningsteam, en zij kijken er grondiger naar voor je. We zijn er om je te helpen! 😊",
            "pt": "Nossa, parece que sua conta pode ter sido fechada por algo como nudez, perfis falsos, golpes ou questões de direitos autorais. Se você acha que pode ser um engano, não se preocupe, estamos com você! 💖 Entre em contato com nossa equipe de suporte, e eles vão dar uma olhada mais de perto para você. Estamos aqui para ajudar! 😊"
        },
        "options": [
            {"text": {"en": "Report and Block", "ar": "الإبلاغ والحظر", "de": "Melden und blockieren", "es": "Reportar y bloquear", "fr": "Signaler et bloquer", "it": "Segnala e blocca", "nl": "Rapporteer en blokkeer", "pt": "Denunciar e bloquear"}, "nextState": "ReportBlockHelp"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "ReportBlockHelp": {
        "messages": {
            "en": "If someone’s behavior doesn’t feel right, don’t hesitate to report or block them—we’re here for you! 💖 Reporting helps us keep our community safe and welcoming for everyone, and blocking ensures they can’t reach out to you anymore. You’ve got this! 😊",
            "ar": "إذا شعرت أن سلوك شخص ما غير مناسب، لا تتردد في الإبلاغ عنه أو حظره—نحن هنا من أجلك! 💖 الإبلاغ يساعدنا في الحفاظ على مجتمعنا آمنًا ومرحبًا للجميع، وحظر المستخدم يضمن أنه لن يتمكن من التواصل معك مجددًا. أنت قادر على التعامل مع هذا! 😊",
            "de": "Falls dir das Verhalten von jemandem nicht gefällt, zögere nicht, ihn zu melden oder zu blockieren – wir sind für dich da! 💖 Melden hilft uns, unsere Gemeinschaft sicher und einladend für alle zu halten, und Blockieren stellt sicher, dass die Person dich nicht mehr kontaktieren kann. Du schaffst das! 😊",
            "es": "Si el comportamiento de alguien no te parece correcto, no dudes en reportarlo o bloquearlo, ¡estamos contigo! 💖 Reportar nos ayuda a mantener nuestra comunidad segura y acogedora para todos, y bloquear asegura que esa persona no pueda contactarte más. ¡Tú puedes con esto! 😊",
            "fr": "Si le comportement de quelqu’un ne te semble pas correct, n’hésite pas à le signaler ou à le bloquer, on est là pour toi ! 💖 Signaler nous aide à garder notre communauté sûre et accueillante pour tout le monde, et bloquer garantit que cette personne ne pourra plus te contacter. Tu gères ! 😊",
            "it": "Se il comportamento di qualcuno non ti sembra giusto, non esitare a segnalarlo o bloccarlo, siamo qui per te! 💖 Segnalare ci aiuta a mantenere la nostra comunità sicura e accogliente per tutti, e bloccare assicura che quella persona non possa più contattarti. Ce la fai! 😊",
            "nl": "Als iemands gedrag niet goed voelt, aarzel dan niet om diegene te melden of te blokkeren – we staan achter je! 💖 Melden helpt ons om onze gemeenschap veilig en gastvrij te houden voor iedereen, en blokkeren zorgt ervoor dat die persoon geen contact meer met je kan opnemen. Jij kunt dit! 😊",
            "pt": "Se o comportamento de alguém não parecer certo, não hesite em denunciar ou bloquear essa pessoa, estamos ao seu lado! 💖 Denunciar nos ajuda a manter nossa comunidade segura e acolhedora para todos, e bloquear garante que essa pessoa não poderá mais entrar em contato com você. Você consegue! 😊"
        },
        "options": [
            {"text": {"en": "Privacy & Safety", "ar": "الخصوصية والسلامة", "de": "Datenschutz & Sicherheit", "es": "Privacidad y seguridad", "fr": "Confidentialité et sécurité", "it": "Privacy e sicurezza", "nl": "Privacy & veiligheid", "pt": "Privacidade e segurança"}, "nextState": "PrivacySafetyHelp"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "PrivacySafetyHelp": {
        "messages": {
            "en": "Your privacy and safety mean the world to us! 💖 It’s a good idea to keep personal details like your contact info private until you feel totally at ease. You can chat safely using the app’s messaging system for now. If anything feels off, just use the report feature—we’re always here for you! 😊",
            "ar": "خصوصيتك وأمانك يعنيان لنا الكثير! 💖 من الأفضل أن تبقي تفاصيلك الشخصية مثل معلومات الاتصال خاصة حتى تشعر بالراحة التامة. يمكنك الدردشة بأمان باستخدام نظام المراسلة في التطبيق في الوقت الحالي. إذا شعرت بأي شيء غير مريح، استخدم ميزة الإبلاغ—نحن دائمًا هنا من أجلك! 😊",
            "de": "Deine Privatsphäre und Sicherheit bedeuten uns alles! 💖 Es ist eine gute Idee, persönliche Daten wie deine Kontaktinformationen für dich zu behalten, bis du dich vollkommen wohl fühlst. Du kannst sicher über das Nachrichtensystem der App chatten. Falls etwas nicht stimmt, nutze einfach die Meldefunktion – wir sind immer für dich da! 😊",
            "es": "¡Tu privacidad y seguridad nos importan muchísimo! 💖 Es buena idea mantener tus datos personales, como tu información de contacto, en privado hasta que te sientas completamente cómodo. Por ahora, puedes charlar con seguridad usando el sistema de mensajería de la app. Si algo no se siente bien, usa la función de reporte, ¡siempre estamos aquí para ti! 😊",
            "fr": "Ta confidentialité et ta sécurité, c’est notre priorité absolue ! 💖 C’est mieux de garder tes infos personnelles, comme tes coordonnées, pour toi jusqu’à ce que tu te sentes totalement à l’aise. Tu peux discuter en toute sécurité avec le système de messagerie de l’app pour l’instant. Si quelque chose te semble bizarre, utilise la fonction de signalement – on est toujours là pour toi ! 😊",
            "it": "La tua privacy e sicurezza ci stanno a cuore! 💖 È una buona idea tenere per te i dettagli personali, come le informazioni di contatto, finché non ti senti completamente a tuo agio. Per ora, puoi chattare in sicurezza usando il sistema di messaggistica dell’app. Se qualcosa non ti sembra giusto, usa la funzione di segnalazione – siamo sempre qui per te! 😊",
            "nl": "Jouw privacy en veiligheid betekenen alles voor ons! 💖 Het is verstandig om persoonlijke gegevens, zoals je contactinformatie, voor jezelf te houden totdat je je helemaal op je gemak voelt. Je kunt nu veilig chatten via het berichtensysteem van de app. Als iets niet goed voelt, gebruik dan de meldingsfunctie – we zijn er altijd voor je! 😊",
            "pt": "Sua privacidade e segurança são tudo para nós! 💖 É uma boa ideia manter seus dados pessoais, como informações de contato, em sigilo até que você se sinta totalmente à vontade. Por enquanto, você pode conversar com segurança usando o sistema de mensagens do app. Se algo parecer estranho, use a função de denúncia – estamos sempre aqui para você! 😊"
        },
        "options": [
            {"text": {"en": "Match Making", "ar": "مطابقة", "de": "Partnervermittlung", "es": "Emparejamiento", "fr": "Rencontres", "it": "Incontri", "nl": "Matchmaking", "pt": "Matchmaking"}, "nextState": "MatchmakingHelp"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "MatchmakingHelp": {
        "messages": {
            "en": "Excited to find a match? It’s so easy! 🎉 Just browse profiles and tap the heart on anyone you like. If they like you back, yay—it’s a match! Then you can start chatting and get to know each other. Have fun! 😊",
            "ar": "متحمس للعثور على تطابق؟ الأمر سهل جدًا! 🎉 تصفح الملفات الشخصية واضغط على القلب لأي شخص يعجبك. إذا أعجبوا بك أيضًا، رائع—إنه تطابق! بعدها يمكنكما البدء في الدردشة والتعرف على بعضكما. استمتع! 😊",
            "de": "Aufgeregt, ein Match zu finden? Es ist ganz einfach! 🎉 Schau dir die Profile an und tippe auf das Herz bei jemandem, der dir gefällt. Wenn sie dich auch mögen, hurra – es ist ein Match! Dann könnt ihr anfangen zu chatten und euch kennenlernen. Viel Spaß! 😊",
            "es": "¿Emocionado por encontrar una pareja? ¡Es súper fácil! 🎉 Explora los perfiles y toca el corazón en quien te guste. Si también te dan like, ¡genial, es un match! Entonces podrán empezar a chatear y conocerse. ¡Diviértete! 😊",
            "fr": "Impatient de trouver un match ? C’est trop facile ! 🎉 Parcours les profils et appuie sur le cœur pour ceux qui te plaisent. S’ils t’aiment en retour, super – c’est un match ! Vous pourrez alors discuter et apprendre à vous connaître. Amuse-toi bien ! 😊",
            "it": "Non vedi l’ora di trovare un match? È facilissimo! 🎉 Sfoglia i profili e tocca il cuore per chi ti piace. Se anche loro ti ricambiano, evviva – è un match! Potrete allora iniziare a chattare e conoscervi meglio. Buon divertimento! 😊",
            "nl": "Enthousiast om een match te vinden? Het is zo makkelijk! 🎉 Blader door de profielen en tik op het hartje bij iemand die je leuk vindt. Als zij jou ook leuk vinden, hoera – het is een match! Dan kunnen jullie gaan chatten en elkaar leren kennen. Veel plezier! 😊",
            "pt": "Ansioso para encontrar um par? É muito fácil! 🎉 Navegue pelos perfis e toque no coração de quem você curtir. Se eles também curtirem você, que legal – é um match! Aí vocês podem começar a conversar e se conhecer melhor. Divirta-se! 😊"
        },
        "options": [
            {"text": {"en": "View Profile", "ar": "عرض الملف الشخصي", "de": "Profil anzeigen", "es": "Ver perfil", "fr": "Voir le profil", "it": "Visualizza profilo", "nl": "Profiel bekijken", "pt": "Ver perfil"}, "nextState": "ViewProfile"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "ViewProfile": {
        "messages": {
            "en": "Hey, want to take a peek at your profile? Just tap 'View Profile' to check out your details. Feeling like a refresh? Hit 'Edit Profile' to update your info and keep it looking great! 😊",
            "ar": "مرحبًا، هل تود إلقاء نظرة على ملفك الشخصي؟ اضغط على 'عرض الملف الشخصي' لترى تفاصيلك. ترغب في تحديثها؟ اضغط على 'تعديل الملف الشخصي' لتجديد معلوماتك وجعلها مميزة! 😊",
            "de": "Hey, möchtest du einen Blick auf dein Profil werfen? Tippe auf 'Profil ansehen', um deine Infos zu sehen. Lust auf eine Auffrischung? Klick auf 'Profil bearbeiten', um deine Daten zu aktualisieren und frisch zu halten! 😊",
            "es": "¡Hola! ¿Quieres echar un vistazo a tu perfil? Toca 'Ver perfil' para revisar tus datos. ¿Te apetece actualizarlos? Presiona 'Editar perfil' para renovar tu información y mantenerla genial! 😊",
            "fr": "Salut ! Envie de jeter un œil à ton profil ? Appuie sur 'Voir le profil' pour voir tes infos. Besoin d’un petit rafraîchissement ? Clique sur 'Modifier le profil' pour mettre à jour tes détails et garder un profil au top ! 😊",
            "it": "Ciao! Vuoi dare un’occhiata al tuo profilo? Tocca 'Visualizza profilo' per vedere i tuoi dati. Ti va di fare un aggiornamento? Premi 'Modifica profilo' per rinnovare le tue info e mantenerle fantastiche! 😊",
            "nl": "Hoi! Wil je je profiel even bekijken? Tik op 'Profiel bekijken' om je gegevens te zien. Zin om het op te frissen? Tik op 'Profiel bewerken' om je info te updaten en het mooi te houden! 😊",
            "pt": "Oi! Quer dar uma espiadinha no seu perfil? Toque em 'Ver Perfil' para conferir suas informações. Quer deixar tudo mais atualizado? Toque em 'Editar Perfil' para atualizar seus dados e deixá-los incríveis! 😊"
        },
        "options": [
            {"text": {"en": "Profile", "ar": "الملف الشخصي", "de": "Profil", "es": "Perfil", "fr": "Profil", "it": "Profilo", "nl": "Profiel", "pt": "Perfil"}, "nextState": "ProfileVerification"},
            {"text": {"en": "No profile", "ar": "لا يوجد ملف تعريف", "de": "Kein Profil", "es": "No tengo perfil", "fr": "Pas de profil", "it": "Nessun profilo", "nl": "Geen profiel", "pt": "Sem perfil"}, "nextState": "NoProfile"}
        ]
    },
    "NoProfile": {
        "messages": {
            "en": "Ready to connect with amazing people on Africa Love Match? Let’s get you started with a profile! Just tap 'Sign Up' to create one—it’s super easy! 😊 Already have a profile? No worries, you can skip this step.",
            "ar": "هل أنت جاهز للتواصل مع أشخاص رائعين على Africa Love Match؟ دعنا نبدأ بإنشاء ملفك الشخصي! اضغط على 'التسجيل' لإنشاء واحد—الأمر سهل جدًا! 😊 لديك ملف شخصي بالفعل؟ لا مشكلة، يمكنك تخطي هذه الخطوة.",
            "de": "Bereit, tolle Leute bei Africa Love Match kennenzulernen? Lass uns mit einem Profil starten! Tippe einfach auf 'Registrieren', um eines zu erstellen – es ist ganz leicht! 😊 Hast du schon ein Profil? Kein Problem, du kannst diesen Schritt überspringen.",
            "es": "¿Listo para conectar con personas increíbles en Africa Love Match? ¡Empecemos creando tu perfil! Solo toca 'Registrarse' para hacer uno, ¡es muy fácil! 😊 ¿Ya tienes un perfil? No te preocupes, puedes saltarte este paso.",
            "fr": "Prêt à rencontrer des personnes géniales sur Africa Love Match ? On va créer ton profil pour commencer ! Appuie sur 'S’inscrire' pour en faire un, c’est vraiment simple ! 😊 Tu as déjà un profil ? Pas de souci, tu peux passer cette étape.",
            "it": "Pronto a conoscere persone fantastiche su Africa Love Match? Iniziamo creando il tuo profilo! Tocca 'Iscriviti' per farne uno, è facilissimo! 😊 Hai già un profilo? Nessun problema, puoi saltare questo passaggio.",
            "nl": "Klaar om leuke mensen te ontmoeten op Africa Love Match? Laten we beginnen met een profiel! Tik op 'Aanmelden' om er een te maken, het is super makkelijk! 😊 Heb je al een profiel? Geen probleem, je kunt deze stap overslaan.",
            "pt": "Pronto para se conectar com pessoas incríveis no Africa Love Match? Vamos começar criando seu perfil! Toque em 'Cadastrar' para fazer o seu, é bem fácil! 😊 Já tem um perfil? Sem problema, você pode pular esta etapa."
        },
        "options": [
            {"text": {"en": "Create profile", "ar": "إنشاء ملف تعريف", "de": "Profil erstellen", "es": "Crear perfil", "fr": "Créer un profil", "it": "Crea profilo", "nl": "Profiel aanmaken", "pt": "Criar perfil"}, "nextState": "ProfileCreation"},
            {"text": {"en": "Subscription", "ar": "اشتراك", "de": "Abonnement", "es": "Suscripción", "fr": "Abonnement", "it": "Abbonamento", "nl": "Abonnement", "pt": "Assinatura"}, "nextState": "SubscriptionHelp"}
        ]
    },
    "ProfileCreation": {
        "messages": {
            "en": "Yay, let’s get you ready to meet awesome new people! 🎉 Tap 'Sign Up' to create your profile—it’s super quick and easy, just a few steps! 😊",
            "ar": "رائع، دعنا نجهزك للتعرف على أشخاص جدد رائعين! 🎉 اضغط على 'التسجيل' لإنشاء ملفك الشخصي—الأمر سريع وسهل جدًا، بضع خطوات فقط! 😊",
            "de": "Super, lass uns dich bereit machen, tolle neue Leute zu treffen! 🎉 Tippe auf 'Registrieren', um dein Profil zu erstellen – es geht ganz schnell und einfach, nur ein paar Schritte! 😊",
            "es": "¡Genial, prepárate para conocer gente nueva increíble! 🎉 Toca 'Registrarse' para crear tu perfil, ¡es súper rápido y fácil, solo unos pocos pasos! 😊",
            "fr": "Génial, on va te préparer à rencontrer de super nouvelles personnes ! 🎉 Appuie sur 'S’inscrire' pour créer ton profil – c’est hyper rapide et facile, juste quelques étapes ! 😊",
            "it": "Fantastico, preparati a conoscere nuove persone straordinarie! 🎉 Tocca 'Iscriviti' per creare il tuo profilo: è velocissimo e facile, solo pochi passaggi! 😊",
            "nl": "Geweldig, laten we je klaarmaken om leuke nieuwe mensen te ontmoeten! 🎉 Tik op 'Aanmelden' om je profiel te maken – het is super snel en makkelijk, maar een paar stappen! 😊",
            "pt": "Oba, vamos te preparar para conhecer novas pessoas incríveis! 🎉 Toque em 'Cadastrar' para criar seu perfil – é bem rápido e fácil, só alguns passos! 😊"
        },
        "options": [
            {"text": {"en": "View Profile", "ar": "عرض الملف الشخصي", "de": "Profil anzeigen", "es": "Ver perfil", "fr": "Voir le profil", "it": "Visualizza profilo", "nl": "Profiel bekijken", "pt": "Ver perfil"}, "nextState": "ViewProfile"},
            {"text": {"en": "Edit profile", "ar": "تعديل الملف الشخصي", "de": "Profil bearbeiten", "es": "Editar perfil", "fr": "Modifier le profil", "it": "Modifica profilo", "nl": "Profiel bewerken", "pt": "Editar perfil"}, "nextState": "ProfileEditHelp"}
        ]
    },
    "ProfileEdit": {
        "messages": {
            "en": "Want to give your profile a little update? It’s easy! 😊 Just head to your profile page and tap the 'Edit' icon to make changes. A quick tip: make sure your photo keeps things friendly and safe—no nudity, violence, celebrity pics, cartoons, or copyrighted stuff. This helps us keep our community awesome for everyone! (Heads up: profiles with inappropriate photos might be removed, so let’s keep it real and respectful!)",
            "ar": "هل ترغب في تحديث ملفك الشخصي قليلاً؟ الأمر سهل! 😊 توجه إلى صفحة ملفك الشخصي واضغط على أيقونة 'تعديل' لإجراء التغييرات. نصيحة صغيرة: تأكد من أن صورتك تحافظ على الأجواء الودودة والآمنة—لا صور عارية، عنف، صور مشاهير، رسومات كرتونية، أو محتوى محمي بحقوق النشر. هذا يساعدنا في الحفاظ على مجتمع رائع للجميع! (تنبيه: الحسابات التي تحتوي على صور غير لائقة قد تُحذف، لذا دعنا نحافظ على الأمور حقيقية ومحترمة!)",
            "de": "Möchtest du dein Profil ein bisschen auffrischen? Das geht ganz leicht! 😊 Geh einfach auf deine Profilseite und tippe auf das 'Bearbeiten'-Symbol, um Änderungen vorzunehmen. Ein kleiner Tipp: Achte darauf, dass dein Foto freundlich und sicher ist – keine Nacktbilder, Gewalt, Promi-Fotos, Cartoons oder urheberrechtlich geschütztes Material. So bleibt unsere Community toll für alle! (Hinweis: Profile mit unangemessenen Fotos könnten entfernt werden, also lass uns alles authentisch und respektvoll halten!)",
            "es": "¿Quieres actualizar un poco tu perfil? ¡Es muy fácil! 😊 Ve a tu página de perfil y toca el ícono de 'Editar' para hacer cambios. Un pequeño consejo: asegúrate de que tu foto sea amigable y segura, sin desnudos, violencia, imágenes de celebridades, caricaturas o contenido con derechos de autor. ¡Esto nos ayuda a mantener nuestra comunidad increíble para todos! (Nota: los perfiles con fotos inapropiadas podrían ser eliminados, así que mantengamos todo real y respetuoso!)",
            "fr": "Envie de rafraîchir ton profil ? C’est très simple ! 😊 Va sur ta page de profil et appuie sur l’icône 'Modifier' pour faire des changements. Un petit conseil : assure-toi que ta photo reste conviviale et sûre – pas de nudité, de violence, de photos de célébrités, de dessins animés ou de contenu protégé par des droits d’auteur. Ça nous aide à garder une communauté géniale pour tout le monde ! (Petit rappel : les profils avec des photos inappropriées pourraient être supprimés, alors restons authentiques et respectueux !)",
            "it": "Vuoi dare un tocco nuovo al tuo profilo? È semplicissimo! 😊 Vai sulla tua pagina profilo e tocca l’icona 'Modifica' per fare le modifiche. Un piccolo consiglio: assicurati che la tua foto sia amichevole e sicura – niente nudità, violenza, immagini di celebrità, cartoni animati o contenuti protetti da copyright. Questo ci aiuta a mantenere la nostra community fantastica per tutti! (Attenzione: i profili con foto non appropriate potrebbero essere rimossi, quindi teniamo tutto reale e rispettoso!)",
            "nl": "Wil je je profiel een beetje opfrissen? Dat is heel makkelijk! 😊 Ga naar je profielpagina en tik op het 'Bewerken'-icoon om aanpassingen te doen. Een kleine tip: zorg ervoor dat je foto vriendelijk en veilig is – geen naakt, geweld, foto’s van beroemdheden, cartoons of materiaal met auteursrecht. Zo houden we onze community fijn voor iedereen! (Let op: profielen met ongepaste foto’s kunnen worden verwijderd, dus laten we het echt en respectvol houden!)",
            "pt": "Quer dar uma atualizada no seu perfil? É bem fácil! 😊 Vá até sua página de perfil e toque no ícone 'Editar' para fazer alterações. Uma dica: certifique-se de que sua foto seja amigável e segura – nada de nudez, violência, imagens de celebridades, desenhos animados ou conteúdo com direitos autorais. Isso ajuda a manter nossa comunidade incrível para todos! (Aviso: perfis com fotos inadequadas podem ser removidos, então vamos manter tudo verdadeiro e respeitoso!)"
        },
        "options": [
            {"text": {"en": "Help", "ar": "مساعدة", "de": "Hilfe", "es": "Ayuda", "fr": "Aide", "it": "Aiuto", "nl": "Hulp", "pt": "Ajuda"}, "nextState": "HelpSelection"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "ProfileVerification": {
        "messages": {
            "en": "Let’s make sure your profile is all set to connect with amazing people on Africa Love Match 😊. You can edit your profile by tapping 'Edit Profile'. You can view your profile by tapping 'View Profile'.",
            "ar": "دعنا نضمن أن ملفك الشخصي جاهز للتواصل مع أشخاص رائعين على Africa Love Match 😊. يمكنك تعديل ملفك بالنقر على 'تعديل الملف الشخصي'. ويمكنك عرض ملفك بالنقر على 'عرض الملف الشخصي'.",
            "de": "Lass uns sicherstellen, dass dein Profil bereit ist, um großartige Menschen bei Africa Love Match zu treffen 😊. Du kannst dein Profil bearbeiten, indem du auf ‚Profil bearbeiten‘ tippst. Du kannst dein Profil ansehen, indem du auf ‚Profil ansehen‘ tippst.",
            "es": "Asegurémonos de que tu perfil esté listo para conectar con personas increíbles en Africa Love Match 😊. Puedes editar tu perfil tocando 'Editar perfil'. Puedes ver tu perfil tocando 'Ver perfil'.",
            "fr": "Assurons-nous que ton profil soit prêt à te connecter avec des personnes formidables sur Africa Love Match 😊. Tu peux modifier ton profil en appuyant sur 'Modifier le profil'. Tu peux consulter ton profil en appuyant sur 'Voir le profil'.",
            "it": "Assicuriamoci che il tuo profilo sia pronto per connetterti con persone straordinarie su Africa Love Match 😊. Puoi modificare il tuo profilo toccando 'Modifica profilo'. Puoi visualizzare il tuo profilo toccando 'Visualizza profilo'.",
            "nl": "Laten we ervoor zorgen dat je profiel klaar is om te verbinden met geweldige mensen op Africa Love Match 😊. Je kunt je profiel bewerken door op 'Profiel bewerken' te tikken. Je kunt je profiel bekijken door op 'Profiel bekijken' te tikken.",
            "pt": "Vamos garantir que seu perfil esteja pronto para se conectar com pessoas incríveis no Africa Love Match 😊. Você pode editar seu perfil tocando em 'Editar perfil'. Você pode ver seu perfil tocando em 'Ver perfil'."
        },
        "options": [
            {"text": {"en": "Edit Profile", "ar": "تعديل الملف الشخصي", "de": "Profil bearbeiten", "es": "Editar perfil", "fr": "Modifier le profil", "it": "Modifica profilo", "nl": "Profiel bewerken", "pt": "Editar perfil"}, "nextState": "ProfileEdit"},
            {"text": {"en": "View Profile", "ar": "عرض الملف الشخصي", "de": "Profil anzeigen", "es": "Ver perfil", "fr": "Voir le profil", "it": "Visualizza profilo", "nl": "Profiel bekijken", "pt": "Ver perfil"}, "nextState": "ViewProfile"}
        ]
    },
    "HelpSelection": {
        "messages": {
            "en": "I’m here to help! 😊 What would you like assistance with today?",
            "ar": "أنا هنا لمساعدتك! 😊 ما الذي تود المساعدة فيه اليوم؟",
            "de": "Ich bin hier, um dir zu helfen! 😊 Wobei möchtest du heute Unterstützung?",
            "es": "¡Estoy aquí para ayudarte! 😊 ¿Con qué te gustaría recibir asistencia hoy?",
            "fr": "Je suis là pour t’aider ! 😊 De quoi as-tu besoin aujourd’hui ?",
            "it": "Sono qui per aiutarti! 😊 Di cosa hai bisogno oggi?",
            "nl": "Ik ben hier om je te helpen! 😊 Waarmee wil je vandaag hulp?",
            "pt": "Estou aqui para te ajudar! 😊 Com o que você gostaria de ajuda hoje?"
        },
        "options": [
            {"text": {"en": "Something Else", "ar": "شيء آخر", "de": "Etwas anderes", "es": "Algo más", "fr": "Autre chose", "it": "Qualcos'altro", "nl": "Iets anders", "pt": "Algo mais"}, "nextState": "SomethingElse"},
            {"text": {"en": "Home", "ar": "الرئيسية", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "nl": "Startpagina", "pt": "Início"}, "nextState": "Initial"}
        ]
    },
    "SomethingElse": {
        "messages": {
            "en": "Please select the category you need help with:",
            "ar": "يرجى اختيار الفئة التي تحتاج إلى مساعدة فيها:",
            "de": "Bitte wähle die Kategorie aus, bei der du Hilfe benötigst:",
            "es": "Por favor, selecciona la categoría con la que necesitas ayuda:",
            "fr": "Veuillez sélectionner la catégorie pour laquelle vous avez besoin d’aide :",
            "it": "Per favore, seleziona la categoria per cui hai bisogno di aiuto:",
            "nl": "Selecteer de categorie waarbij je hulp nodig hebt:",
            "pt": "Por favor, selecione a categoria com a qual você precisa de ajuda:"
        },
        "options": [
            {"text": {"en": "Subscription", "ar": "اشتراك", "de": "Abonnement", "es": "Suscripción", "fr": "Abonnement", "it": "Abbonamento", "nl": "Abonnement", "pt": "Assinatura"}, "nextState": "SubscriptionHelp"},
            {"text": {"en": "Account Closed", "ar": "الحساب مغلق", "de": "Konto geschlossen", "es": "Cuenta cerrada", "fr": "Compte fermé", "it": "Account chiuso", "nl": "Account gesloten", "pt": "Conta encerrada"}, "nextState": "AccountClosedHelp"},
            {"text": {"en": "Profile Edit", "ar": "تحرير الملف الشخصي", "de": "Profil bearbeiten", "es": "Editar perfil", "fr": "Modifier le profil", "it": "Modifica del profilo", "nl": "Profiel bewerken", "pt": "Editar perfil"}, "nextState": "ProfileEdit"},
            {"text": {"en": "Privacy and Safety", "ar": "الخصوصية والأمان", "de": "Datenschutz und Sicherheit", "es": "Privacidad y seguridad", "fr": "Confidentialité et sécurité", "it": "Privacy e sicurezza", "nl": "Privacy en veiligheid", "pt": "Privacidade e segurança"}, "nextState": "PrivacySafetyHelp"},
            {"text": {"en": "Report and Block", "ar": "الإبلاغ والحظر", "de": "Melden und blockieren", "es": "Reportar y bloquear", "fr": "Signaler et bloquer", "it": "Segnala e blocca", "nl": "Rapporteer en blokkeer", "pt": "Denunciar e bloquear"}, "nextState": "ReportBlockHelp"},
            {"text": {"en": "Payment and Refund", "ar": "الدفع والاسترداد", "de": "Zahlung und Rückerstattung", "es": "Pago y reembolso", "fr": "Paiement et remboursement", "it": "Pagamento e rimborso", "nl": "Betaling en terugbetaling", "pt": "Pagamento e reembolso"}, "nextState": "PaymentRefundHelp"},
            {"text": {"en": "Matchmaking", "ar": "التوفيق بين الأشخاص", "de": "Partnervermittlung", "es": "Emparejamiento", "fr": "Mise en relation", "it": "Matchmaking", "nl": "Matchmaking", "pt": "Matchmaking"}, "nextState": "MatchmakingHelp"}
        ]
    }
}

# Initialize session state
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {
        "firstName": "",
        "language": "en",
        "aboutMe": "",
        "current_state": "Initial"
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Helper functions
def complete_setup():
    st.session_state.setup_complete = True
    save_chat_history()

def show_feedback():
    st.session_state.feedback_shown = True
    save_chat_history()

def save_chat_history():
    try:
        chat_data = {
            "userId": st.session_state.profile.get("userId", "anonymous"),
            "timestamp": pd.Timestamp.now(),
            "messages": st.session_state.messages,
            "language": st.session_state.profile["language"]
        }
        st.session_state.chat_history.append(chat_data)
        chat_df = pd.DataFrame(st.session_state.chat_history)
        chat_df.to_csv(os.path.join(data_dir, "chat_history.csv"), index=False)
        logger.info("Chat history saved successfully")
    except Exception as e:
        logger.error(f"Error saving chat history: {e}")

# Setup phase for collecting user profile
if not st.session_state.setup_complete:
    st.set_page_config(page_title="Africa Love Match FAQ Chatbot", page_icon="💖")
    st.title("IMARA: Africa Love Match FAQ Chatbot")

    st.subheader("Profile Information")
    st.session_state.profile["firstName"] = st.text_input(
        label="First Name",
        value=st.session_state.profile["firstName"],
        placeholder="Enter your first name",
        max_chars=40
    )
    st.session_state.profile["language"] = st.selectbox(
        "Select Language",
        options=["English", "Arabic", "German", "Spanish", "French", "Italian", "Dutch", "Portuguese"],
        index=["English", "Arabic", "German", "Spanish", "French", "Italian", "Dutch", "Portuguese"].index(
            {"en": "English", "ar": "Arabic", "de": "German", "es": "Spanish", "fr": "French", "it": "Italian", "nl": "Dutch", "pt": "Portuguese"}.get(st.session_state.profile["language"], "English")
        )
    )
    st.session_state.profile["aboutMe"] = st.text_area(
        label="About Me",
        value=st.session_state.profile["aboutMe"],
        placeholder="Tell us about yourself (e.g., hobbies, interests)",
        max_chars=200
    )

    if st.button("Start Chatting", on_click=complete_setup):
        st.session_state.profile["userId"] = f"user_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        st.write("Profile setup complete. Let’s chat with IMARA! 😊")

# Chat phase
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:
    st.set_page_config(page_title="Africa Love Match FAQ Chatbot", page_icon="💖")
    st.title("IMARA: Africa Love Match FAQ Chatbot")

    # Check for soccer enthusiast
    soccer_keywords = ["soccer", "football"]
    is_soccer_enthusiast = any(keyword in st.session_state.profile["aboutMe"].lower() for keyword in soccer_keywords)
    if is_soccer_enthusiast:
        st.info("Hey, a soccer fan! ⚽ Ready to connect with fellow Africa Soccer Kings enthusiasts? Ask IMARA anything! 😊")
    else:
        st.info("Welcome to Africa Love Match! 😊 Ask IMARA about subscriptions, profiles, or anything else!")

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=config.get("openai_api_key", st.secrets.get("OPENAI_API_KEY")))
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        st.error("Unable to connect to the chatbot service. Please check your API key.")
        st.stop()

    # Map language selection to FAQ language codes
    language_map = {
        "English": "en", "Arabic": "ar", "German": "de", "Spanish": "es",
        "French": "fr", "Italian": "it", "Dutch": "nl", "Portuguese": "pt"
    }
    lang_code = language_map[st.session_state.profile["language"]]

    # Initialize system prompt
    if not st.session_state.messages:
        system_prompt = (
            f"You are IMARA, a friendly assistant for Africa Love Match, helping {st.session_state.profile['firstName']} "
            f"with FAQs in their preferred language ({st.session_state.profile['language']}). "
            f"Use the provided FAQ responses to answer questions accurately and conversationally. "
            f"If the user mentions soccer or football, add a friendly nod to Africa Soccer Kings. "
            f"Keep responses concise, friendly, and professional, using emojis like 😊 and 💖. "
            f"Here are the FAQ responses:\n{str(FAQ_RESPONSES)}"
        )
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        # Display initial greeting
        initial_message = FAQ_RESPONSES["Initial"]["messages"][lang_code]
        if is_soccer_enthusiast:
            initial_message += f" Loving the soccer vibe, {st.session_state.profile['firstName']}! ⚽ Ready to connect with Africa Soccer Kings fans?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Display FAQ options as buttons
    current_state = st.session_state.profile["current_state"]
    if current_state in FAQ_RESPONSES:
        st.subheader("Quick Options")
        cols = st.columns(3)
        for idx, option in enumerate(FAQ_RESPONSES[current_state]["options"]):
            with cols[idx % 3]:
                if st.button(option["text"][lang_code]):
                    st.session_state.profile["current_state"] = option["nextState"]
                    response = FAQ_RESPONSES[option["nextState"]]["messages"][lang_code]
                    if is_soccer_enthusiast and any(keyword in response.lower() for keyword in soccer_keywords):
                        response += " By the way, loving your soccer passion! ⚽"
                    st.session_state.messages.append({"role": "user", "content": option["text"][lang_code]})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.user_message_count += 1
                    st.rerun()

    # Handle user input
    if st.session_state.user_message_count < 5:
        if prompt := st.chat_input("Your question or message", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if st.session_state.user_message_count < 4:
                with st.chat_message("assistant"):
                    try:
                        stream = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            stream=True
                        )
                        response = st.write_stream(stream)
                        if is_soccer_enthusiast and any(keyword in prompt.lower() for keyword in soccer_keywords):
                            response += f" Loving the soccer spirit, {st.session_state.profile['firstName']}! ⚽ Connect with more Africa Soccer Kings fans!"
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        logger.error(f"Error generating OpenAI response: {e}")
                        st.error("Sorry, something went wrong. Please try again!")
                        st.session_state.messages.append({"role": "assistant", "content": "Sorry, something went wrong. Please try again! 😊"})
            st.session_state.user_message_count += 1
            save_chat_history()

    # Check if chat is complete
    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True
        save_chat_history()

# Feedback phase
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get Feedback", on_click=show_feedback):
        st.write("Fetching feedback...")

if st.session_state.feedback_shown:
    st.subheader("Feedback")
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg["role"] != "system"])
    
    try:
        feedback_client = OpenAI(api_key=config.get("openai_api_key", st.secrets.get("OPENAI_API_KEY")))
        feedback_completion = feedback_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    f"You are a helpful tool providing feedback on a user's interaction with IMARA, the Africa Love Match FAQ chatbot. "
                    f"Give a score from 1 to 10 based on how well the user engaged with the chatbot (e.g., clarity of questions, relevance to FAQs). "
                    f"Follow this format:\n"
                    f"Overall Score: //Your score\n"
                    f"Feedback: //Your feedback\n"
                    f"Do not ask questions or engage further."
                )},
                {"role": "user", "content": f"Conversation history:\n{conversation_history}"}
            ]
        )
        st.write(feedback_completion.choices[0].message.content)
    except Exception as e:
        logger.error(f"Error generating feedback: {e}")
        st.error("Unable to generate feedback. Please try again later.")

    if st.button("Restart Chat", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")