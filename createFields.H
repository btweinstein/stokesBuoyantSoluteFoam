Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

#include "createPhi.H"


label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, simple.dict(), pRefCell, pRefValue);
mesh.setFluxRequired(p.name());


Info<< "Reading Transport Properties... \n" << endl;
IOdictionary transportProperties
(
     IOobject
     (
        "transportProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ_IF_MODIFIED,
        IOobject::NO_WRITE
     )
);


Info<< "Reading dynamic viscosity mu \n" << endl;
dimensionedScalar mu
(
     transportProperties.lookup("mu")
 );

Info<< "Reading kinematic viscosity nu \n" << endl;
dimensionedScalar nu
(
     transportProperties.lookup("nu")
 );


