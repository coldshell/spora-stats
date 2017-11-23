#!/usr/bin/octave
csv_office = dlmread("../../csv/office-step-2000.csv", ",");
csv_pdf = dlmread("../../csv/pdf-step-2000.csv", ",");
csv_autocad = dlmread("../../csv/autocad-step-2000.csv", ",");
csv_db = dlmread("../../csv/db-step-2000.csv", ",");
csv_img = dlmread("../../csv/img-step-2000.csv", ",");
csv_archive = dlmread("../../csv/archive-step-2000.csv", ",");

# Get encrypted files
office = csv_office(2:end, 4);
pdf = csv_pdf(2:end, 5);
autocad = csv_autocad(2:end, 6);
db = csv_db(2:end, 7);
img = csv_img(2:end, 8);
archive = csv_archive(2:end, 9);

# Get prices
office_price = csv_office(2:end, 10);
pdf_price = csv_pdf(2:end, 10);
autocad_price = csv_autocad(2:end, 10);
db_price = csv_db(2:end, 10);
img_price = csv_img(2:end, 10);
archive_price = csv_archive(2:end, 10);


#
# Plot data
#
f = figure('Name', 'Spora Stats');

# Plots
hold on;
grid on;
plot(office, office_price, "k")
plot(pdf, pdf_price, "r");
plot(autocad, autocad_price, "b");
plot(db, db_price, "g");
plot(img, img_price, "m");
plot(archive, archive_price, "c");
hold off;

# Labels
xlabel("Number of encrypted files");
ylabel("Price");
legend('office', 'pdf', 'autocad', 'db', 'img', 'archive');


# pause
waitfor(f)
