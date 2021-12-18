from gensim.summarization import keywords
import spacy
from textacy import preprocessing
from textacy import extract

nlp = spacy.load("en_core_web_lg")


#
# Clean text, remove stop words chuck in with ngrams and extract keywords. 
# Try using SpaCy.io and textacy
# Resource: https://stackoverflow.com/questions/53598243/is-there-a-bi-gram-or-tri-gram-feature-in-spacy
#

text = "About the job\nDescription\n\nWe’re seeking an experienced product leader to join us in our Boston, MA office to lead product management for AWS’s newest hybrid storage service. AWS Outposts provide fully managed AWS infrastructure and services to customers in their on-premises data centers. Amazon S3 on Outposts, launched in 2020, provides hybrid object storage enabling customers to store and retrieve data on-premises using the S3 programming model and features.\n\nOur team is responsible for delivering this hybrid storage platform on Outposts. As part of the team, you will help shape object storage for the next generation hybrid computing platform.\n\nProduct Management at AWS is an opportunity to collaborate with engineering, design, and business development teams. We are looking for an entrepreneurial product leader who is passionate about delivering solutions to customers and excited about growing a new AWS business. Successful candidates will be able to build strategic roadmap for the business, dive into technical details working closely with the engineering team and drive the delivery of features that will delight our customers.\n\nYou will be joining an experienced team of engineers and product managers who have built and scaled services at Amazon and beyond. We’re looking for a new teammate who is enthusiastic, empathetic, curious, motivated, reliable, and able to collaborate effectively with a diverse team of peers.\n\nWork/Life Balance\n\nOur team puts a high value on work-life balance. Our entire team is co-located in the Boston Seaport office, but we’re also flexible when people occasionally need to work from home. We generally keep core in-office hours from 10am to 4pm.\n\nMentorship and Career Growth\n\nOur team is dedicated to supporting new team members. Our team has a broad mix of experience levels and Amazon tenures, and we’re building an environment that celebrates knowledge sharing and mentorship. Our senior members truly enjoy mentoring others through one-on-one sessions helping them with their career growth.\n\nInclusive Team Culture\n\nHere at AWS, we embrace our differences. We are committed to furthering our culture of inclusion. We have ten employee-led affinity groups, reaching 40,000 employees in over 190 chapters globally. We have innovative benefit offerings, and we host annual and ongoing learning experiences, including our Conversations on Race and Ethnicity (CORE) and AmazeCon (gender diversity) conferences. Amazon’s culture of inclusion is reinforced within our 14 Leadership Principles, which remind team members to seek diverse perspectives, learn and be curious, and earn trust\n\n\nBasic Qualifications\nBachelor’s Degree in Computer Science or related field.\n10+ years of product management experience including defining product vision, roadmap and driving product investment decisions.\n10+ years of work experience with launching large scale software products and driving adoption.\nDemonstrable experience delivering through large teams.\nDemonstrable experience delivering strategies and insights to VP-level leadership.\n\nPreferred Qualifications\n\nAmazon is committed to a diverse and inclusive workforce. Amazon is an equal opportunity employer and does not discriminate on the basis of race, ethnicity, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status. For individuals with disabilities who would like to request an accommodation, please visit https://www.amazon.jobs/en/disability/us\n\n\nCompany - Amazon Dev Center U.S., Inc.\n\nJob ID: A1584516"


preproc = preprocessing.make_pipeline(
    preprocessing.remove.html_tags, 
    preprocessing.normalize.whitespace
)

doc = nlp(text)

ngrams = list(extract.basics.ngrams(doc, 2, min_freq=1))
print(ngrams)

#print(keywords(text))


