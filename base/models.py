from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


COUNTRIES = [
    ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burundi', 'Burundi'),
    ('Cabo Verde', 'Cabo Verde'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Canada', 'Canada'),
    ('Central African Republic', 'Central African Republic'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo, Republic of the', 'Congo, Republic of the'),
    ('Congo, Democratic Republic of the', 'Congo, Democratic Republic of the'),
    ('Costa Rica', 'Costa Rica'),
    ('Côte d’Ivoire', 'Côte d’Ivoire'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Eswatini', 'Eswatini'),
    ('Ethiopia', 'Ethiopia'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('Gabon', 'Gabon'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Greece', 'Greece'),
    ('Grenada', 'Grenada'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Honduras', 'Honduras'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran', 'Iran'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Korea, North', 'Korea, North'),
    ('Korea, South', 'Korea, South'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Laos', 'Laos'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libya', 'Libya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mexico', 'Mexico'),
    ('Micronesia', 'Micronesia'),
    ('Moldova', 'Moldova'),
    ('Monaco', 'Monaco'),
    ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Myanmar (Burma)', 'Myanmar (Burma)'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('North Macedonia', 'North Macedonia'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Palestine', 'Palestine'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Qatar', 'Qatar'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Rwanda', 'Rwanda'),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
    ('Saint Lucia', 'Saint Lucia'),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tome and Principe', 'Sao Tome and Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', 'Senegal'),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syria', 'Syria'),
    ('Taiwan', 'Taiwan'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania', 'Tanzania'),
    ('Thailand', 'Thailand'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tonga', 'Tonga'),
    ('Trinidad and Tobago', 'Trinidad and Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Vatican City', 'Vatican City'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe'),
]

VISA_TYPES = [
    ('Aufenthaltserlaubnis zum Zweck der Ausbildung (Section 16a)', 'Aufenthaltserlaubnis zum Zweck der Ausbildung (Section 16a)'),
    ('Aufenthaltserlaubnis für ein Studium (Section 16b)', 'Aufenthaltserlaubnis für ein Studium (Section 16b)'),
    ('Aufenthaltserlaubnis zur Arbeitsplatzsuche für qualifizierte Fachkräfte (Section 16c)', 'Aufenthaltserlaubnis zur Arbeitsplatzsuche für qualifizierte Fachkräfte (Section 16c)'),
    ('Aufenthaltserlaubnis für Sprachkurse und Schulbesuch (Section 16d)', 'Aufenthaltserlaubnis für Sprachkurse und Schulbesuch (Section 16d)'),
    ('Aufenthaltserlaubnis für Forschung und Wissenschaft (Section 16e)', 'Aufenthaltserlaubnis für Forschung und Wissenschaft (Section 16e)'),
    ('Aufenthaltserlaubnis für Fachkräfte mit Berufsausbildung (Section 18a)', 'Aufenthaltserlaubnis für Fachkräfte mit Berufsausbildung (Section 18a)'),
    ('Aufenthaltserlaubnis für Fachkräfte mit akademischer Ausbildung (Section 18b)', 'Aufenthaltserlaubnis für Fachkräfte mit akademischer Ausbildung (Section 18b)'),
    ('Aufenthaltserlaubnis für Forscher (Section 18c)', 'Aufenthaltserlaubnis für Forscher (Section 18c)'),
    ('Aufenthaltserlaubnis für Selbständige (Section 18d)', 'Aufenthaltserlaubnis für Selbständige (Section 18d)'),
    ('Aufenthaltserlaubnis für freiberufliche Tätigkeit (Section 18e)', 'Aufenthaltserlaubnis für freiberufliche Tätigkeit (Section 18e)'),
    ('Blaue Karte EU (Section 19a)', 'Blaue Karte EU (Section 19a)'),
    ('Aufenthaltserlaubnis für Hochqualifizierte (Section 19b)', 'Aufenthaltserlaubnis für Hochqualifizierte (Section 19b)'),
    ('Aufenthaltserlaubnis für IT-Fachkräfte (Section 19c)', 'Aufenthaltserlaubnis für IT-Fachkräfte (Section 19c)'),
    ('Aufenthaltserlaubnis für Forschende und Lehrende (Section 20)', 'Aufenthaltserlaubnis für Forschende und Lehrende (Section 20)'),
    ('Aufenthaltserlaubnis für Unternehmer (Section 21)', 'Aufenthaltserlaubnis für Unternehmer (Section 21)'),
    ('Aufenthaltserlaubnis aus humanitären Gründen (Section 25)', 'Aufenthaltserlaubnis aus humanitären Gründen (Section 25)'),
    ('Aufenthaltserlaubnis für ehemalige Deutsche (Section 26)', 'Aufenthaltserlaubnis für ehemalige Deutsche (Section 26)'),
    ('Aufenthaltserlaubnis für Familiennachzug zu Deutschen (Section 28)', 'Aufenthaltserlaubnis für Familiennachzug zu Deutschen (Section 28)'),
    ('Aufenthaltserlaubnis für Familiennachzug zu Ausländern (Section 29)', 'Aufenthaltserlaubnis für Familiennachzug zu Ausländern (Section 29)'),
    ('Aufenthaltserlaubnis für Ehegattennachzug (Section 30)', 'Aufenthaltserlaubnis für Ehegattennachzug (Section 30)'),
    ('Aufenthaltserlaubnis für geschiedene Ehegatten (Section 31)', 'Aufenthaltserlaubnis für geschiedene Ehegatten (Section 31)'),
    ('Aufenthaltserlaubnis für Kinder (Section 32)', 'Aufenthaltserlaubnis für Kinder (Section 32)'),
    ('Aufenthaltserlaubnis für andere Familienangehörige (Section 33)', 'Aufenthaltserlaubnis für andere Familienangehörige (Section 33)'),
    ('Aufenthaltserlaubnis für Pflegekinder (Section 34)', 'Aufenthaltserlaubnis für Pflegekinder (Section 34)'),
    ('Niederlassungserlaubnis für Jugendliche (Section 35)', 'Niederlassungserlaubnis für Jugendliche (Section 35)'),
    ('Aufenthaltserlaubnis für Eltern (Section 36)', 'Aufenthaltserlaubnis für Eltern (Section 36)'),
    ('Niederlassungserlaubnis für ehemalige Deutsche (Section 38)', 'Niederlassungserlaubnis für ehemalige Deutsche (Section 38)'),
    ('Daueraufenthaltserlaubnis-EU (Section 38a)', 'Daueraufenthaltserlaubnis-EU (Section 38a)'),
    ('Aufenthaltserlaubnis für langfristig Aufenthaltsberechtigte in der EU (Section 39)', 'Aufenthaltserlaubnis für langfristig Aufenthaltsberechtigte in der EU (Section 39)'),
]

HOURS_CHOICES = [
    ('09:00', '09:00'),
    ('10:00', '10:00'),
    ('11:00', '11:00'),
    ('12:00', '12:00'),
    ('13:00', '13:00'),
    ('14:00', '14:00'),
    ('15:00', '15:00'),
    ('16:00', '16:00'),
    ('17:00', '17:00'),
]

GERMAN_CITIES_CHOICES = [
    ('Berlin', 'Berlin'),
    ('Hamburg', 'Hamburg'),
    ('Munich', 'Munich'),
    ('Cologne', 'Cologne'),
    ('Frankfurt', 'Frankfurt'),
    ('Stuttgart', 'Stuttgart'),
    ('Düsseldorf', 'Düsseldorf'),
    ('Dortmund', 'Dortmund'),
    ('Essen', 'Essen'),
    ('Leipzig', 'Leipzig'),
    ('Bremen', 'Bremen'),
    ('Dresden', 'Dresden'),
    ('Hanover', 'Hanover'),
    ('Nuremberg', 'Nuremberg'),
    ('Duisburg', 'Duisburg'),
    ('Bochum', 'Bochum'),
    ('Wuppertal', 'Wuppertal'),
    ('Bielefeld', 'Bielefeld'),
    ('Bonn', 'Bonn'),
    ('Münster', 'Münster'),
    ('Karlsruhe', 'Karlsruhe'),
    ('Mannheim', 'Mannheim'),
    ('Augsburg', 'Augsburg'),
    ('Wiesbaden', 'Wiesbaden'),
    ('Gelsenkirchen', 'Gelsenkirchen'),
    ('Mönchengladbach', 'Mönchengladbach'),
    ('Braunschweig', 'Braunschweig'),
    ('Chemnitz', 'Chemnitz'),
    ('Kiel', 'Kiel'),
    ('Aachen', 'Aachen'),
    ('Halle', 'Halle'),
    ('Magdeburg', 'Magdeburg'),
    ('Freiburg', 'Freiburg'),
    ('Krefeld', 'Krefeld'),
    ('Lübeck', 'Lübeck'),
    ('Oberhausen', 'Oberhausen'),
    ('Erfurt', 'Erfurt'),
    ('Mainz', 'Mainz'),
    ('Rostock', 'Rostock'),
    ('Kassel', 'Kassel'),
    ('Hagen', 'Hagen'),
    ('Saarbrücken', 'Saarbrücken'),
    ('Hamm', 'Hamm'),
    ('Mülheim', 'Mülheim'),
    ('Potsdam', 'Potsdam'),
    ('Ludwigshafen', 'Ludwigshafen'),
    ('Oldenburg', 'Oldenburg'),
    ('Leverkusen', 'Leverkusen'),
    ('Osnabrück', 'Osnabrück'),
    ('Solingen', 'Solingen'),
    ('Heidelberg', 'Heidelberg'),
    ('Herne', 'Herne'),
    ('Neuss', 'Neuss'),
    ('Darmstadt', 'Darmstadt'),
    ('Paderborn', 'Paderborn'),
    ('Regensburg', 'Regensburg'),
    ('Ingolstadt', 'Ingolstadt'),
    ('Würzburg', 'Würzburg'),
    ('Wolfsburg', 'Wolfsburg'),
    ('Offenbach', 'Offenbach'),
    ('Ulm', 'Ulm'),
    ('Heilbronn', 'Heilbronn'),
    ('Pforzheim', 'Pforzheim'),
    ('Göttingen', 'Göttingen'),
    ('Bottrop', 'Bottrop'),
    ('Trier', 'Trier'),
    ('Recklinghausen', 'Recklinghausen'),
    ('Reutlingen', 'Reutlingen'),
    ('Bremerhaven', 'Bremerhaven'),
    ('Koblenz', 'Koblenz'),
    ('Bergisch Gladbach', 'Bergisch Gladbach'),
    ('Jena', 'Jena'),
    ('Remscheid', 'Remscheid'),
    ('Erlangen', 'Erlangen'),
    ('Moers', 'Moers'),
    ('Siegen', 'Siegen'),
    ('Hildesheim', 'Hildesheim'),
    ('Salzgitter', 'Salzgitter'),
]

phone_regex = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=50, choices=COUNTRIES, help_text="Select your country")
    current_city = models.CharField(max_length=50, choices=GERMAN_CITIES_CHOICES, help_text="Select your current city")
    passport_number = models.CharField(max_length=14, unique=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True, null=True)
    type_of_visa = models.CharField(max_length=85, choices=VISA_TYPES)
    appointment_date = models.DateField(null=True)
    appointment_time = models.CharField(max_length=5, choices=HOURS_CHOICES)
    token = models.CharField(max_length=10, unique=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_got_appointment = models.BooleanField(default=False)
    appointment_created_at = models.DateTimeField(auto_now_add=True)
    appointment_updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.is_reviewed:
            user_subject = 'Your appointment request has reviewed!'
            user_context = {
                'full_name': self.full_name,
            }
            user_message = render_to_string('appointment_reviewed.html', user_context)
            user_email = EmailMessage(user_subject, user_message, settings.EMAIL_HOST_USER, [self.email])
            user_email.content_subtype = 'html'
            user_email.send()