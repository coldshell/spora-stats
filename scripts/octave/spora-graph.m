csv_autocad = dlmread("../../csv/office-pdf.csv", ";");

office = csv_autocad(:, 6);
pdf = csv_autocad(:, 5);
% autocad = csv(:, 6);
% db = csv(:, 7);
% img = csv(:, 8);
% archive = csv(:, 9);
price = csv_autocad(:, 10);

hold on;

xlabel("Number of encrypted PDF");
ylabel("Number of encrypted *");
zlabel("Price");

scatter3(pdf, office, price, 10, "r", "filled");
saveas(1, "figure.png");
% scatter3(pdf, autocad, price, 10, "b", "filled");
% scatter3(pdf, db, price, 10, "g", "filled");
% scatter3(pdf, img, price, 10, 80, "filled");
% scatter3(pdf, archive, price, 10, 10, "filled");

hold off;
