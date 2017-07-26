/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011-2016 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    simpleFoam

Description
    Steady-state solver for incompressible, turbulent flow, using the SIMPLE
    algorithm.

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "simpleControl.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "postProcess.H"

    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"
    #include "createControl.H"
    #include "createFields.H"
    #include "initContinuityErrs.H"
  
    while (runTime.run())
    {
        runTime++;

        Info<< "Time = " << runTime.timeName() << nl << endl;
        //Make sure the deltaT increment on c is reasonable...
        Info << "deltaT: " << c.mesh().time().deltaT() << nl << endl;

        //*** Calculate the concentration field ***

        while (simple.correctNonOrthogonal())
        {
            fvScalarMatrix cEqn
            (
                fvm::ddt(c)
              + fvm::div(phi, c)
              - fvm::laplacian(D_star, c)
            );
            cEqn.solve();
        }

        //*** Calculate the velocity field***

        double U_res_init = 1;
        double P_res_init = 1;
	
    	rhok = Ra*c;

        int stokes_iter = 0;

	    // Force both conditions to true to ensure at least one iteration is attempted.
	    bool gt_res = true;
	    bool lt_max_iter = true;
		
        while(gt_res && lt_max_iter)
        {
            p_rgh.storePrevIter();

            // --- Pressure-velocity SIMPLE corrector
            {
                #include "UEqn.H"
                #include "pEqn.H"
            }

            Info << "Finished stokes iteration " << stokes_iter << endl;

            stokes_iter++;

            // Recalculate the termination conditions
            gt_res = (U_res_init > U_converged) || (P_res_init > p_converged);
            lt_max_iter = (stokes_iter <= max_stokes_iter);
        }
        
        if(!lt_max_iter) // i.e. ran out of iterations
        {
	        Info<< "Ran for maximum number of stokes iterations." << endl;
	    }
	    Info<< "Stokes solver converged in " << stokes_iter - 1 << " iterations." << nl << endl;

        #include "CourantNo.H"

        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;	
    }

    Info<< "End\n" << endl;
    
    return 0;
}


// ************************************************************************* //
